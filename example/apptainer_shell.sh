ml load apptainer
export NGC_API_KEY=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
export LOCAL_NIM_CACHE=~/.cache/nim
docker_sifs_path=/projects/m000018/docker/
mkdir -p "$LOCAL_NIM_CACHE"
apptainer shell --nv \
  --bind "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  --bind "apptainer_nim_copy:/opt/nim" \
  --bind "/projects/m000018:/projects/m000018" \
  --env NGC_API_KEY=$NGC_API_KEY \
  $docker_sifs_path/rfdiffusion.sif
