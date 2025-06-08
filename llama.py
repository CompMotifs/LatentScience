from pathlib import Path
from typing import Optional

import modal

DEFAULT_DEEPSEEK_R1_ARGS = [  # good default llama.cpp cli args for deepseek-r1
    "--cache-type-k",
    "q4_0",
    "--threads",
    "12",
    "-no-cnv",
    "--prio",
    "2",
    "--temp",
    "0.6",
    "--ctx-size",
    "8192",
]

app = modal.App("example-llama-cpp")


@app.local_entrypoint()
def main(
    prompt: Optional[str] = None,
    model: str = "DeepSeek-R1",  # or "phi-4"
    n_predict: int = -1,  # max number of tokens to predict, -1 is infinite
    args: Optional[str] = None,  # string of arguments to pass to llama.cpp's cli
):
    """Run llama.cpp inference on Modal for phi-4 or deepseek r1."""
    import shlex

    org_name = "unsloth"
    # two sample models: the diminuitive phi-4 and the chonky deepseek r1
    if model.lower() == "phi-4":
        model_name = "phi-4-GGUF"
        quant = "Q2_K"
        model_entrypoint_file = f"phi-4-{quant}.gguf"
        model_pattern = f"*{quant}*"
        revision = None
        parsed_args = DEFAULT_PHI_ARGS if args is None else shlex.split(args)
    elif model.lower() == "deepseek-r1":
        model_name = "DeepSeek-R1-GGUF"
        quant = "UD-IQ1_S"
        model_entrypoint_file = (
            f"{model}-{quant}/DeepSeek-R1-{quant}-00001-of-00003.gguf"
        )
        model_pattern = f"*{quant}*"
        revision = "02656f62d2aa9da4d3f0cdb34c341d30dd87c3b6"
        parsed_args = DEFAULT_DEEPSEEK_R1_ARGS if args is None else shlex.split(args)
    else:
        raise ValueError(f"Unknown model {model}")

    repo_id = f"{org_name}/{model_name}"
    download_model.remote(repo_id, [model_pattern], revision)

    # call out to a `.remote` Function on Modal for inference
    result = llama_cpp_inference.remote(
        model_entrypoint_file,
        prompt,
        n_predict,
        parsed_args,
        store_output=model.lower() == "deepseek-r1",
    )
    output_path = Path("/tmp") / f"llama-cpp-{model}.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"🦙 writing response to {output_path}")
    output_path.write_text(result)


LLAMA_CPP_RELEASE = "b4568"
MINUTES = 60

cuda_version = "12.4.0"  # should be no greater than host CUDA version
flavor = "devel"  #  includes full CUDA toolkit
operating_sys = "ubuntu22.04"
tag = f"{cuda_version}-{flavor}-{operating_sys}"


image = (
    modal.Image.from_registry(f"nvidia/cuda:{tag}", add_python="3.12")
    .apt_install("git", "build-essential", "cmake", "curl", "libcurl4-openssl-dev")
    .run_commands("git clone https://github.com/ggerganov/llama.cpp")
    .run_commands(
        "cmake llama.cpp -B llama.cpp/build "
        "-DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON "
    )
    .run_commands(  # this one takes a few minutes!
        "cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli"
    )
    .run_commands("cp llama.cpp/build/bin/llama-* llama.cpp")
    .entrypoint([])  # remove NVIDIA base container entrypoint
)

model_cache = modal.Volume.from_name("llamacpp-cache", create_if_missing=True)
cache_dir = "/root/.cache/llama.cpp"

download_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("huggingface_hub[hf_transfer]==0.26.2")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)


@app.function(
    image=download_image, volumes={cache_dir: model_cache}, timeout=30 * MINUTES
)
def download_model(repo_id, allow_patterns, revision: Optional[str] = None):
    from huggingface_hub import snapshot_download

    print(f"🦙 downloading model from {repo_id} if not present")

    snapshot_download(
        repo_id=repo_id,
        revision=revision,
        local_dir=cache_dir,
        allow_patterns=allow_patterns,
    )

    model_cache.commit()  # ensure other Modal Functions can see our writes before we quit

    print("🦙 model loaded")