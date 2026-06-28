add_executable(cuda_hello hello_cuda.cu)
set_target_properties(cuda_hello PROPERTIES
  CUDA_STANDARD 17
  CUDA_STANDARD_REQUIRED ON
  CUDA_EXTENSIONS OFF
)

add_executable(vector_addition vector_addition.cu)
set_target_properties(vector_addition PROPERTIES
  CUDA_STANDARD 17
  CUDA_STANDARD_REQUIRED ON
  CUDA_EXTENSIONS OFF
)

add_executable(vector_addition_2 vector_addition_2.cu)
set_target_properties(vector_addition_2 PROPERTIES
  CUDA_STANDARD 17
  CUDA_STANDARD_REQUIRED ON
  CUDA_EXTENSIONS OFF
)

add_executable(vector_addition_3 vector_addition_3.cu)
set_target_properties(vector_addition_3 PROPERTIES
  CUDA_STANDARD 17
  CUDA_STANDARD_REQUIRED ON
  CUDA_EXTENSIONS OFF
)
