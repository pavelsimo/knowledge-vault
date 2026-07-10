add_executable(runtime_api runtime_api.cu)
set_target_properties(runtime_api PROPERTIES
  CUDA_STANDARD 17
  CUDA_STANDARD_REQUIRED ON
  CUDA_EXTENSIONS OFF
)
