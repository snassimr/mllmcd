import argparse
import asyncio
import json
from typing import Optional
import tensorrt_llm
from colored import cprint
from tensorrt_llm._utils import mpi_barrier, mpi_rank, mpi_world_size
from tensorrt_llm.executor import SamplingParams
from mpi4py import MPI
import uvicorn
import torch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from tensorrt_llm.bindings.executor import ExecutorConfig
from tensorrt_llm.executor import ExecutorBindingsWorker, GenerationResult

tensorrt_llm.logger.set_level('info')

TP_SIZE = 2
PP_SIZE = 1  # Assuming no pipeline parallelism, update if necessary
TIMEOUT_KEEP_ALIVE = 5  # seconds
TIMEOUT_TO_PREVENT_DEADLOCK = 1  # seconds
app = FastAPI()
executor: Optional[ExecutorBindingsWorker] = None


@app.get("/stats")
async def stats() -> Response:
    assert executor is not None
    return JSONResponse(json.loads(await executor.aget_stats()))


@app.get("/health")
async def health() -> Response:
    """Health check."""
    return Response(status_code=200)


@app.post("/generate")
async def generate(request: Request) -> Response:
    if executor is None:
        return JSONResponse({"error": "Executor is not initialized"}, status_code=503)
    executor.block_subordinates()

    request_dict = await request.json()

    sampling_params = SamplingParams(max_new_tokens=request_dict.get("max_tokens", 500), temperature=request_dict.get("temperature", 0.5),
                                     top_p=request_dict.get("top_p", 0.89), top_k=request_dict.get("top_k", 50),
                                     repetition_penalty=request_dict.get("repetition_penalty", 1.05),
                                     frequency_penalty=request_dict.get("frequency_penalty", 0.2),
                                     presence_penalty=request_dict.get("presence_penalty", 0.6))
    prompt = request_dict.pop("prompt", "")

    cprint(f"Prompt: {prompt}", "green")
    output = executor.generate(prompt, sampling_params=sampling_params)
    cprint(f"Output: {output}", "green")
    cprint(f"Output DIR: {dir(output)}", "blue")

    # mpi_barrier()
    return JSONResponse({"texts": output.text})


def initialize_executor(args, mpi_rank):
    global executor
    cprint(f"Initializing executor for rank {mpi_rank}", "green")
    executor_config = ExecutorConfig(max_beam_width=args.max_beam_width)
    torch.cuda.set_device(mpi_rank)

    hf_model_dir = args.hf_model_dir
    engine_dir = args.engine_dir
    tokenizer_dir = hf_model_dir

    mpi_barrier()
    tensorrt_llm.logger.warning(f"Build finished for rank {mpi_rank}")
    executor = ExecutorBindingsWorker(engine_dir, tokenizer_dir, executor_config)
    cprint("Executor created", "green")


async def start_server(args):
    config = uvicorn.Config(app, host=args.host, port=args.port, log_level="info",
                            timeout_keep_alive=TIMEOUT_KEEP_ALIVE)
    server = uvicorn.Server(config)
    await server.serve()


async def main(args):
    mpi_rank = MPI.COMM_WORLD.Get_rank()
    world_size = MPI.COMM_WORLD.Get_size()
    cprint(f"MPI rank: {mpi_rank}, world size: {world_size}", "green")
    if world_size != TP_SIZE * PP_SIZE:
        raise ValueError("MPI world size must be equal to TP_SIZE * PP_SIZE")

    if mpi_rank < TP_SIZE:
        initialize_executor(args, mpi_rank)

    if mpi_rank == 0:
        await start_server(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf_model_dir", type=str, required=True,
                        help="Read the model data and tokenizer from this directory")
    parser.add_argument("--engine_dir", type=str, required=True, help="Directory to save and load the engine.")
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--max_beam_width", type=int, default=1)
    parser.add_argument("--max_tokens", type=int, default=200)
    args = parser.parse_args()
    # set MPI world size to 2

    cprint(f"MPI COMM WORLD SIZE: {dir(MPI.COMM_WORLD)}", "green")
    cprint(f"MPI COMM WORLD SIZE: {MPI.COMM_WORLD.Get_size()}", "green")
    asyncio.run(main(args))