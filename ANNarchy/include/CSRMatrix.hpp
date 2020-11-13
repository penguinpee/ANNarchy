/*
 *
 *    CSRMatrix.hpp
 *
 *    This file is part of ANNarchy.
 *
 *    Copyright (C) 2020  Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>,
 *    Julien Vitay <julien.vitay@gmail.com>
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
 *  @brief      Implementation of a *compressed sparse row* (CSR) format.
 *  @details    Probably the most common sparse matrix format in computer science. The major idea is that only nonzeros are
 *              stored in a long continuous array and a second array provides a lookup, which slice in this array contains
 *              to a row.
 *
 *              Let's consider the following example matrix
 * 
 *                      | 0 1 0 |
 *                  A = | 2 0 3 |
 *                      | 0 0 0 |
 *                      | 0 0 4 |
 * 
 *              So the array containing the column indices would be:
 * 
 *                  col_idx_ = [ 1 , 0, 3, 3 ]
 *
 *              And the row assignment would be:
 * 
 *                  row_begin_ = [ 0, 1, 3, 3, 4 ]
 * 
 *              So the i-th row in the matrix reaches from row_begin_[i] to row_begin_[i+1] and could select the column indices.
 *              As visible on the third row, an empty row is indicated if both values are equal. So, contrary to the LIL which does
 *              not store empty rows, the CSR does. We therefore need the post_ranks_ array to have a mapping between LIL indices
 *              and matrix rows.
 * 
 *  @tparam     IT      data type to represent the ranks within the matrix. Generally unsigned data types should be chosen.
 *                      The data type determines the maximum size of the matrix:
 * 
 *                      - unsigned char (1 byte):        [0 .. 255]
 *                      - unsigned short int (2 byte):   [0 .. 65.535]
 *                      - unsigned int (4 byte):         [0 .. 4.294.967.295]
 * 
 *              The chosen data type should be able to represent the maximum values (LILMatrix::num_rows_ and ::num_columns_)
 */
template<typename IT = unsigned int>
class CSRMatrix {

  protected:
    std::vector<IT> post_ranks_;    ///< Needed to translate LIL indices to row_indicies.
    std::vector<IT> row_begin_;     ///< i-th element marks the begin of the i-th row
    std::vector<IT> col_idx_;       ///< contains the column indices in row major order order. To access row i, get indices from row_begin_.

    unsigned int num_rows_;         ///< number of rows in the dense matrix
    unsigned int num_columns_;      ///< number of columns in the dense matrix

  public:
    unsigned int num_non_zeros_;    ///< number of nonzeros

    explicit CSRMatrix(const unsigned int num_rows, const unsigned int num_columns):
        num_rows_(num_rows), num_columns_(num_columns) {

        row_begin_ = std::vector<IT>(num_rows+1, 0);
        col_idx_ = std::vector<IT>();
        num_non_zeros_ = 0;
    }

    void init_matrix_from_lil(std::vector<IT> row_indices, std::vector< std::vector<IT> > column_indices) {
        post_ranks_ = row_indices;
        auto lil_row_idx = 0;

        for ( auto r = 0; r < num_rows_; r++ ) {
            row_begin_[r] = col_idx_.size();

            // check if this row is in list
            if (r == row_indices[lil_row_idx]) {
                col_idx_.insert(col_idx_.end(), column_indices[lil_row_idx].begin(), column_indices[lil_row_idx].end());
                num_non_zeros_ += column_indices[lil_row_idx].size();

                // next row in LIL
                lil_row_idx++;
            }
        }
        row_begin_[num_rows_] = col_idx_.size();

        // sanity check
        if (lil_row_idx != row_indices.size())
            std::cerr << "something went wrong ..." << std::endl;
        if (num_non_zeros_ != col_idx_.size())
            std::cerr << "something went wrong ... " << num_non_zeros_ << std::endl;
    }

    //
    //  Connectivity patterns
    //
    void fixed_number_pre_pattern(std::vector<IT> post_ranks, std::vector<IT> pre_ranks, unsigned int nnz_per_row, std::mt19937& rng) {
        // Generate post_to_pre LIL
        auto lil_mat = new LILMatrix<IT>(this->num_rows_, this->num_columns_);
        lil_mat->fixed_number_pre_pattern(post_ranks, pre_ranks, nnz_per_row, rng);

        // Generate CSRC_T from this LIL
        init_matrix_from_lil(lil_mat->get_post_rank(), lil_mat->get_pre_ranks());

        // cleanup
        delete lil_mat;
    }

    void fixed_probability_pattern(std::vector<IT> post_ranks, std::vector<IT> pre_ranks, double p, bool allow_self_connections, std::mt19937& rng) {
        // Generate post_to_pre LIL
        auto lil_mat = new LILMatrix<IT>(this->num_rows_, this->num_columns_);
        lil_mat->fixed_probability_pattern(post_ranks, pre_ranks, p, allow_self_connections, rng);

        // Generate CSRC_T from this LIL
        init_matrix_from_lil(lil_mat->get_post_rank(), lil_mat->get_pre_ranks());

        // cleanup
        delete lil_mat;
    }

    //
    //  Connectivity Accessor
    //
    std::vector<int> get_post_rank() { return post_ranks_; }

    std::vector<int> get_dendrite_pre_rank(int lil_idx) {
        IT row_idx = post_ranks_[lil_idx];
        auto beg = col_idx_.begin() + row_begin_[row_idx];
        auto end = col_idx_.begin() + row_begin_[row_idx+1];
        return std::vector<IT>(beg, end);
    }

    int nb_synapses(int lil_idx) {
        int post_rank = post_ranks_[lil_idx];
        return (row_begin_[post_rank+1] - row_begin_[post_rank]);
    }

    //
    //  Initialize Variables
    //
    template <typename VT>
    std::vector<VT> init_matrix_variable(VT default_value) {
        return std::vector<VT>(num_non_zeros_, default_value);
    }

    template <typename VT>
    std::vector<VT> init_matrix_variable_uniform(VT a, VT b, std::mt19937& rng) {
    #ifdef _DEBUG
        std::cout << "CSRMatrix::initialize_variable_uniform(): arguments = (" << a << ", " << b << ") and num_non_zeros_ = " << num_non_zeros_ << std::endl;
    #endif
        std::uniform_real_distribution<VT> dis (a,b);
        auto new_variable = std::vector<VT>(num_non_zeros_, 0.0);
        std::generate(new_variable.begin(), new_variable.end(), [&]{ return dis(rng); });
        return new_variable;
    }

    template <typename VT>
    std::vector<VT> init_matrix_variable_normal(VT mean, VT sigma, std::mt19937& rng) {
    #ifdef _DEBUG
        std::cout << "Initialize variable with Normal(" << mean << ", " << sigma << ")" << std::endl;
    #endif
        std::normal_distribution<VT> dis (mean, sigma);
        auto new_variable = std::vector<VT>(num_non_zeros_, 0.0);
        std::generate(new_variable.begin(), new_variable.end(), [&]{ return dis(rng); });
        return new_variable;
    }

    //
    //  Update Variables
    //
    template <typename VT>
    inline void update_matrix_variable(std::vector<VT> &variable, const IT row_idx, const IT column_idx, const VT value) {
        for(int j = row_begin_[row_idx]; j < row_begin_[row_idx+1]; j++) {
            if ( col_idx_[j] == column_idx ) {
                variable[j] = value;
                break;
            }
        }
    }

    template <typename VT>
    inline void update_matrix_variable_row(std::vector<VT> &variable, const IT lil_idx, const std::vector<VT> data) {
        IT row_idx = post_ranks_[lil_idx];
        std::copy(data.begin(), data.end(), variable.begin() + row_begin_[row_idx]);
    }

    template <typename VT>
    inline void update_matrix_variable_all(std::vector<VT> &variable, const std::vector< std::vector<VT> > &data) 
    {
        if (data.size() != post_ranks_.size())
            std::cerr << "Update variable failed: mismatch of data field sizes." << std::endl;

        for (auto i = 0; i < post_ranks_.size(); i++) {
            update_matrix_variable_row(variable, i, data[i]);
        }
    }

    template <typename VT>
    inline VT get_matrix_variable(const std::vector<VT> &variable, const IT row_idx, const IT column_idx) {
        for(int j = row_begin_[row_idx]; j < row_begin_[row_idx+1]; j++)
            if ( col_idx_[j] == column_idx )
                return variable[j];
        return 0; // should not happen ...
    }

    template <typename VT>
    inline std::vector< VT > get_matrix_variable_row(const std::vector<VT> &variable, const IT lil_idx) {
        IT row_idx = post_ranks_[lil_idx];
        auto beg = variable.begin()+row_begin_[row_idx];
        auto end = variable.begin()+row_begin_[row_idx+1];
        return std::vector<VT>(beg, end);
    }

    template <typename VT>
    inline std::vector< std::vector <VT> > get_matrix_variable_all(const std::vector<VT> &variable) {
        auto values = std::vector< std::vector <VT> >();
        for (unsigned int lil_idx=0; lil_idx < post_ranks_.size(); lil_idx++) {
            values.push_back(std::move(get_matrix_variable_row(variable, lil_idx)));
        }
        return values;
    }

    /**
     *  @brief      Initialize a vector variable
     *  @details    Variables marked as 'semiglobal' stored in a vector of the size of LILMatrix::post_rank
     *  @tparam     VT              data type of the variable.
     *  @param[in]  default_value   value to initialize all elements in the vector
     */
    template <typename VT>
    inline std::vector<VT> init_vector_variable(VT default_value) {
        return std::vector<VT>(post_ranks_.size(), default_value);
    }

    /**
     *  @brief      Initialize a vector variable
     *  @details    Variables marked as 'semiglobal' stored in a vector of the size of LILMatrix::post_rank
     *  @tparam     VT          data type of the variable.
     *  @param[in]  values      new values for the row indicated by lil_idx.
     */
    template <typename VT>
    inline void update_vector_variable_all(std::vector<VT> &variable, std::vector<VT> values) {
        assert ( (variable.size() == values.size()) );

        std::copy(values.begin(), values.end(), variable.begin());
    }

    template <typename VT>
    inline void update_vector_variable(std::vector<VT> &variable, int lil_idx, VT value) {
        assert( (lil_idx < post_ranks_.size()) );

        variable[lil_idx] = value;
    }

    /**
     *  @brief      Get a vector variable
     *  @details    Variables marked as 'semiglobal' stored in a vector of the size of LILMatrix::post_rank
     *  @tparam     VT          data type of the variable.
     */
    template <typename VT>
    inline std::vector<VT> get_vector_variable_all(std::vector<VT> variable) {
        return variable;
    }

    /**
     *  @brief      Get a single item from a vector variable
     *  @details    Variables marked as 'semiglobal' stored in a vector of the size of LILMatrix::post_rank
     *  @tparam     VT          data type of the variable.
    */
    template <typename VT>
    inline VT get_vector_variable(std::vector<VT> variable, int lil_idx) {
        assert( (lil_idx < post_ranks_.size()) );

        return variable[lil_idx];
    }

    virtual ~CSRMatrix() {
    #ifdef _DEBUG
        std::cout << "CSRMatrix::~CSRMatrix()" << std::endl;
    #endif
        clear();
    }

    void clear() {
    #ifdef _DEBUG
        std::cout << "CSRMatrix::clear()" << std::endl;
    #endif
        std::fill(row_begin_.begin(), row_begin_.end(), 0);
        col_idx_.clear();
        col_idx_.shrink_to_fit();
        num_non_zeros_ = 0;
    }

    friend std::ostream& operator<< (std::ostream& os, const CSRMatrix<IT>& matrix) {
        os << "-- Store a " << matrix.num_rows_ << " times " << matrix.num_columns_ << " Matrix in CSR format --" << std::endl;
        os << "row_idx:" << std::endl;
        os << "[ ";
        for(auto it = matrix.row_begin_.begin(); it != matrix.row_begin_.end(); it++) {
            os << *it << " ";
        }
        os << "]" << std::endl;

        os << "col_idx:" << std::endl;
        os << "[ ";
        for(auto it = matrix.col_idx_.begin(); it != matrix.col_idx_.end(); it++)
            os << *it << " ";
        os << "]" << std::endl;

        return os;
    }

    friend std::ostream& operator<< (std::ostream& os, CSRMatrix<IT>* matrix) {
        return os << *matrix;
    }

    // Returns size in bytes for connectivity
    size_t size_in_bytes() {
        size_t size = 3 * sizeof(unsigned int);

        size += row_begin_.capacity() * sizeof(IT);
        size += col_idx_.capacity() * sizeof(IT);
        size += post_ranks_.capacity() * sizeof(IT);
        return size;
    }
};