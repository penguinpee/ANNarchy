/*
 *
 *    CSRCMatrixCUDA.hpp
 *
 *    This file is part of ANNarchy.
 *
 *    Copyright (C) 2020-21  Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>
 *
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    ANNarchy is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

/**
 *  @brief      Implementation of the *compressed sparse row and column* format on CUDA devices.
 *  @details    For more details on the format please refer to CSRCMatrix.
 */
template<typename IT = unsigned int>
class CSRCMatrixCUDA: public CSRCMatrix<IT> {

public:
    // CSR forward view
    IT* gpu_post_rank;
    IT* gpu_row_ptr;
    IT* gpu_pre_rank;

    // backward view
    IT* gpu_col_ptr;
    IT* gpu_row_idx;
    IT* gpu_inv_idx;

    CSRCMatrixCUDA<IT>(const IT num_rows, const IT num_columns) : CSRCMatrix<IT>(num_rows, num_columns) {
    }

    void init_matrix_from_lil(std::vector<IT> &row_indices, std::vector< std::vector<IT> > &column_indices) {
    #ifdef _DEBUG
        std::cout << "CSRCMatrixCUDA::init_matrix_from_lil() " << std::endl;
    #endif
        // host side
        static_cast<CSRCMatrix<IT>*>(this)->init_matrix_from_lil(row_indices, column_indices);

        //
        // Copy data
        cudaMalloc((void**)&gpu_post_rank, this->post_ranks_.size()*sizeof(IT));
        cudaMemcpy(gpu_post_rank, this->post_ranks_.data(), this->post_ranks_.size()*sizeof(IT), cudaMemcpyHostToDevice);

        cudaMalloc((void**)&gpu_row_ptr, this->row_begin_.size()*sizeof(IT));
        cudaMemcpy(gpu_row_ptr, this->row_begin_.data(), this->row_begin_.size()*sizeof(IT), cudaMemcpyHostToDevice);

        cudaMalloc((void**)&gpu_pre_rank, this->col_idx_.size()*sizeof(IT));
        cudaMemcpy(gpu_pre_rank, this->col_idx_.data(), this->col_idx_.size()*sizeof(IT), cudaMemcpyHostToDevice);

        cudaMalloc((void**)&gpu_col_ptr, this->_col_ptr.size()*sizeof(IT));
        cudaMemcpy(gpu_col_ptr, this->_col_ptr.data(), this->_col_ptr.size()*sizeof(IT), cudaMemcpyHostToDevice);

        cudaMalloc((void**)&gpu_row_idx, this->_row_idx.size()*sizeof(IT));
        cudaMemcpy(gpu_row_idx, this->_row_idx.data(), this->_row_idx.size()*sizeof(IT), cudaMemcpyHostToDevice);

        cudaMalloc((void**)&gpu_inv_idx, this->_inv_idx.size()*sizeof(IT));
        cudaMemcpy(gpu_inv_idx, this->_inv_idx.data(), this->_inv_idx.size()*sizeof(IT), cudaMemcpyHostToDevice);

        auto err = cudaGetLastError();
        if (err != cudaSuccess) {
            std::cerr << "CSRMatrixCUDA::init_matrix_from_lil: " << cudaGetErrorString(err) << std::endl;
        }

    }

    //
    //  Variables
    //
    template <typename VT>
    VT* init_matrix_variable_gpu(const std::vector<VT> &host_variable) {
        VT* gpu_variable;
        cudaMalloc((void**)&gpu_variable, this->num_non_zeros_*sizeof(VT));
        cudaMemcpy(gpu_variable, host_variable.data(), this->num_non_zeros_*sizeof(VT), cudaMemcpyHostToDevice);

        return gpu_variable;
    }

    template <typename VT>
    VT* init_vector_variable_gpu(const std::vector<VT> &host_variable) {
        VT* gpu_variable;
        cudaMalloc((void**)&gpu_variable, this->post_ranks_.size() * sizeof(VT));
        cudaMemcpy(gpu_variable, host_variable.data(), this->post_ranks_.size() * sizeof(VT), cudaMemcpyHostToDevice);

        return gpu_variable;
    }

    //
    // Read-out variables from GPU and return as LIL
    //
    template <typename VT>
    std::vector<std::vector<VT>> get_device_matrix_variable_as_lil(VT* gpu_variable) {
        auto host_tmp = std::vector<std::vector<VT>>();

        auto flat_data = std::vector<VT>(this->num_non_zeros_, 0.0);
        cudaMemcpy(flat_data.data(), gpu_variable, this->num_non_zeros_*sizeof(VT), cudaMemcpyDeviceToHost);

        for (auto post_rk = this->post_ranks_.cbegin(); post_rk != this->post_ranks_.cend(); post_rk++) {
            host_tmp.push_back(std::vector<VT>(flat_data.begin()+this->row_begin_[*post_rk], flat_data.begin()+this->row_begin_[*post_rk+1]));
        }
        return host_tmp;
    }
};