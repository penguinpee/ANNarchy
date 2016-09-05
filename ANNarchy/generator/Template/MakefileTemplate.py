# Linux, Seq or OMP
linux_omp_template = """# Makefile generated by ANNarchy
all:
\tcython -%(py_major)s ANNarchyCore%(net_id)s.pyx --cplus
\t%(compiler)s %(cpu_flags)s -shared -fPIC -fpermissive -std=c++11  %(openmp)s \\
        *.cpp -o ANNarchyCore%(net_id)s.so \\
        %(python_include)s -I%(numpy_include)s -I%(cython_ext)s \\
        %(python_lib)s %(libs)s
\t mv ANNarchyCore%(net_id)s.so ../..

clean:
\trm -rf *.o
\trm -rf *.so
"""

# Linux, CUDA
linux_cuda_template = """# Makefile generated by ANNarchy
all:
\tcython -%(py_major)s ANNarchyCore%(net_id)s.pyx --cplus
\tnvcc %(cuda_gen)s %(gpu_flags)s -std=c++11 -lineinfo -Xcompiler -fPIC -shared \\
        ANNarchyHost.cu *.cpp -o ANNarchyCore%(net_id)s.so \\
        %(python_include)s -I%(numpy_include)s -I%(cython_ext)s\\
        -lpython%(py_version)s  %(libs)s
\t mv ANNarchyCore%(net_id)s.so ../..

clean:
\trm -rf *.o
\trm -rf *.so
"""

# OSX, Seq only
osx_seq_template = """# Makefile generated by ANNarchy
all:
\tcython -%(py_major)s ANNarchyCore%(net_id)s.pyx --cplus
\t%(compiler)s -stdlib=libc++ -std=c++11 -fPIC -shared %(cpu_flags)s -fpermissive \\
        *.cpp -o ANNarchyCore%(net_id)s.so \\
        %(python_include)s -I%(numpy_include)s -I%(cython_ext)s\\
        %(python_lib)s %(libs)s
\t mv ANNarchyCore%(net_id)s.so ../..

clean:
\trm -rf *.o
\trm -rf *.so
"""

# CudaCheck module, build during setup process
cuda_check = """all: cuda_check.so

cuda_check_cu.o:
\tnvcc -c cuda_check.cu -Xcompiler -fPIC -o cuda_check_cu.o

cuda_check.cpp:
\tcython --cplus cuda_check.pyx

cuda_check.so: cuda_check_cu.o cuda_check.cpp
\tg++ cuda_check.cpp -fPIC -shared -g -I. %(py_include)s cuda_check_cu.o -lcudart -o cuda_check.so

clean:
\trm -f cuda_check_cu.o
\trm -f cuda_check.cpp
\trm -f cuda_check.so
"""