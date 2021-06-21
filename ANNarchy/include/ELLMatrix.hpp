/*
 * ELLMatrix.hpp
 *
 * Copyright (c) 2020 Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 2.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

/**
 *  \brief      ELLPACK sparse matrix representation according to Kincaid et al. 1989 with some
 *              minor modifications as described below.
 * 
 *  \details    The ELLPACK format encodes the nonzeros of a sparse matrix in dense matrices
 *              where one represent the column indices and another one for each variable.
 *
 *              Let's consider the following example matrix
 * 
 *                      | 0 1 0 |
 *                  A = | 2 0 3 |
 *                      | 0 0 0 |
 *                      | 0 0 4 |
 *
 *              First we need to determine the maximum number of column-entries per row (we
 *              call this *maxnzr*), in our example 2.
 * 
 *              Then we read out the column entries and fill the created dense matrix from
 *              left. Important is the encoding of non-existing entries some authors suggest -1
 *              but this would require every time a check if a contained index is valid. We
 *              fill non-existing places with 0.
 * 
 *                              | 1 0 |
 *                  col_idx_ =  | 0 2 |
 *                              | 2 0 |
 * 
 *              To allow learning on the matrix and encoding of 0 as existing value, we also
 *              introduce a row-length array (rl):
 * 
 *                  rl_ = [ 1, 2, 1 ]
 * 
 *              As for LILMatrix and others one need to highlight that rows with no nonzeros are
 *              compressed.
 *
 *  \tparam     IT          index type
 *  \tparam     row_major   determines the matrix storage for the dense sub matrices. If
 *                          set to true, the matrix will be stored as row major, otherwise
 *                          in column major. 
 *                          Please note that the original format stores in row-major to ensure a
 *                          partial caching of data on CPUs. The column-major ordering is only
 *                          intended for the usage on GPUs.
 */
template<typename IT=unsigned int, bool row_major=true>
class ELLMatrix {
protected:
    IT maxnzr_;                     ///< maximum row length of nonzeros
    const IT num_rows_;             ///< maximum number of rows
    const IT num_columns_;          ///< maximum number of columns

    std::vector<IT> post_ranks_;    ///< which rows does contain entries
    std::vector<IT> col_idx_;       ///< column indices for accessing dense vector
    std::vector<IT> rl_;            ///< number of nonzeros in each row
public:
    /**
     *  \brief      Constructor
     *  \details    Does not initialize any data.
     *  \param[in]  num_rows        number of rows of the original matrix (this value is only provided to have an unified interface)
     *  \param[in]  num_columns     number of columns of the original matrix (this value is only provided to have an unified interface)
     */
    ELLMatrix(const IT num_rows, const IT num_columns):
        num_rows_(num_rows), num_columns_(num_columns) {
    }

    virtual ~ELLMatrix() {
    #ifdef _DEBUG
        std::cout << "ELLMatrix::~ELLMatrix()" << std::endl;
    #endif
        clear();
    }

    void clear() {
    #ifdef _DEBUG
        std::cout << "ELLMatrix::clear()" << std::endl;
    #endif
        post_ranks_.clear();
        post_ranks_.shrink_to_fit();

        col_idx_.clear();
        col_idx_.shrink_to_fit();

        rl_.clear();
        rl_.shrink_to_fit();

        maxnzr_ = 0;
    }

    inline IT get_maxnzr() {
        return maxnzr_;
    }

    inline IT* get_rl() {
        return rl_.data();
    }

    inline IT* get_column_indices() {
        return col_idx_.data();
    }

    /**
     *  @details    get row indices
     *  @returns    a list of row indices for all rows comprising of at least one element
     */
    std::vector<IT> get_post_rank() {
        return post_ranks_;
    }

    /**
     *  @details    get column indices
     *  @returns    a list-in-list of column indices for all rows comprising of at least one element sorted by rows.
     */
    std::vector<std::vector<IT>> get_pre_ranks() { 
        auto pre_ranks = std::vector<std::vector<IT>>();

        if (row_major) {
            for(IT r = 0; r < post_ranks_.size(); r++) {
                auto beg = col_idx_.begin() + r*maxnzr_;
                auto end = col_idx_.begin() + r*maxnzr_ + rl_[r];
                pre_ranks.push_back(std::vector<IT>(beg, end));
            }
        } else {
            std::cerr << "ELLMatrix::get_pre_ranks() is not implemented for column major" << std::endl;
        }
        return pre_ranks;
    }

    /**
     *  @details    get column indices of a specific row.
     *  @param[in]  lil_idx     index of the selected row. To get the correct index use the post_rank array, e. g. lil_idx = post_ranks.find(row_idx).
     *  @returns    a list of column indices of a specific row.
     */
    std::vector<IT> get_dendrite_pre_rank(int lil_idx) {
        assert( (lil_idx < post_ranks_.size()) );

        if (row_major) {
            auto beg = col_idx_.begin() + lil_idx*maxnzr_;
            auto end = col_idx_.begin() + lil_idx*maxnzr_ + rl_[lil_idx];

            return std::vector<IT>(beg, end);
        } else {
            auto tmp = std::vector < IT >(rl_[lil_idx]);
            int num_rows = post_ranks_.size();
            for (int c = 0; c < rl_[lil_idx]; c++) {
                tmp[c] = col_idx_[c*num_rows+lil_idx];
            }
            return tmp;
        }
    }

    /**
     *  @details    returns the stored connections in this matrix
     *  @returns    number of synapses across all rows
     */
    size_t nb_synapses() {
        int size = 0;
        for (auto it = rl_.begin(); it != rl_.end(); it++) {
            size += *it;
        }

        return size;
    }

    /**
     *  @details    returns the stored connections in this matrix for a given row. The return type is an unsigned int as the maximum of small data types used for IT could be exceeded.
     *  @param[in]  lil_idx     index of the selected row. To get the correct index use the post_rank array, e. g. lil_idx = post_ranks.find(row_idx).
     *  @returns    number of synapses across all rows of a given row.
     */
    IT nb_synapses(IT lil_idx) {
        assert( (lil_idx < post_ranks_.size()) );

        return rl_[lil_idx];
    }

    /**
     *  @details    returns the number of stored rows. The return type is an unsigned int as the maximum of small data types used for IT could be exceeded.
     *  @returns    the number of stored rows (i. e. each of these rows contains at least one connection).
     */
    IT nb_dendrites() {
        return post_ranks_.size();
    }

    /**
     *  @brief      initialize connectivity based on a provided LIL representation.
     *  @details    First we scan *pre_ranks* to determine the value maxnzr_. Then we convert pre_ranks.
     *  @todo       Currently we ignore post_ranks ...
     */
    void init_matrix_from_lil(std::vector<IT> &post_ranks, std::vector< std::vector<IT> > &pre_ranks) {
    #ifdef _DEBUG
        std::cout << "ELLMatrix::init_matrix_from_lil()" << std::endl;
    #endif
        assert( (post_ranks.size() == pre_ranks.size()) );

        //
        // 1st step:    iterate across the LIL to identify maximum
        //              row length
        post_ranks_ = post_ranks;
        maxnzr_ = std::numeric_limits<IT>::min();
        rl_ = std::vector<IT>(post_ranks.size());

        auto pre_it = pre_ranks.begin();
        IT idx = 0;

        for(; pre_it != pre_ranks.end(); pre_it++, idx++) {
            rl_[idx] = pre_it->size();
        }

        maxnzr_ = *std::max_element(rl_.begin(), rl_.end());

        //
        // 2nd step:    iterate across the LIL to copy indices
        //
        // Contrary to many reference implementations we take 0 here but we have rl_
        // to encode the "real" row length.
        if (row_major) {
            col_idx_ = std::vector<IT>(maxnzr_ * post_ranks_.size(), 0);

            pre_it = pre_ranks.begin();
            idx = 0;

            for(; pre_it != pre_ranks.end(); pre_it++, idx++) {
                size_t col_off = idx * maxnzr_;
                for (auto col_it = pre_it->begin(); col_it != pre_it->end(); col_it++) {
                    col_idx_[col_off++] = *col_it;
                }
            }

        } else {
            int num_rows = post_ranks_.size();
            col_idx_ = std::vector<IT>(maxnzr_ * num_rows, 0);

            for (int r = 0; r < num_rows; r++) {
                int c = 0;
                for (auto col_it = pre_ranks[r].begin(); col_it != pre_ranks[r].end(); col_it++, c++) {
                    col_idx_[c*num_rows+r] = *col_it;
                }
            }
        }
    #ifdef _DEBUG
        std::cout << "created ELLMatrix:" << std::endl;
        this->print_matrix_statistics();
    #endif
    }

    /**
     *  @details    Initialize a num_rows_ by num_columns_ matrix based on the stored connectivity.
     *  @tparam     VT              data type of the variable.
     *  @param[in]  default_value   the default value for all nonzeros in the matrix.
     *  @returns    Determines a flattened dense matrix of dimension num_rows_ times maxnzr_
     */
    template <typename VT>
    std::vector< VT > init_matrix_variable(VT default_value) {
    #ifdef _DEBUG
        std::cout << "Initialize variable with constant " << default_value << std::endl;
    #endif
        return std::vector<VT> (post_ranks_.size() * maxnzr_, default_value);
    }

    template <typename VT>
    inline void update_matrix_variable_all(std::vector<VT> &variable, const std::vector< std::vector<VT> > &data) {
        assert( (post_ranks_.size() == data.size()) );
        assert( (rl_.size() == data.size()) );

        if (row_major) {
            for(IT r = 0; r < post_ranks_.size(); r++) {
                assert( (rl_[r] == data[r].size()) );
                auto beg = variable.begin() + r*maxnzr_;

                std::copy(data[r].begin(), data[r].end(), beg);
            }


        } else {
            int num_rows = post_ranks_.size();
            for(IT r = 0; r < num_rows; r++) {
                assert( (rl_[r] == data[r].size()) );

                for(IT c = 0; c < rl_[r]; c++) {
                    variable[c*num_rows+r] = data[r][c];
                }
            }
        }
    }

    template <typename VT>
    inline void update_matrix_variable_row(std::vector<VT> &variable, const IT lil_idx, const std::vector<VT> data) {
        if (row_major) {
            assert( (rl_[lil_idx] == data.size()) );

            auto beg = variable.begin() + lil_idx*maxnzr_;
            std::copy(data.begin(), data.end(), beg);
        } else {
            std::cerr << "ELLMatrix::update_matrix_variable_row() is not implemented for column major" << std::endl;
        }
    }

    template <typename VT>
    inline void update_matrix_variable(std::vector<VT> &variable, const IT row_idx, const IT column_idx, const VT value) {
        std::cerr << "ELLMatrix::update_matrix_variable() is not implemented" << std::endl;
    }
   
    /**
     *  @brief      retrieve a LIL representation for a given variable.
     *  @details    this function is only called by the Python interface retrieve the current value of a *local* variable.
     *  @tparam     VT          data type of the variable.
     *  @returns    a LIL representation from the given variable.
     */
    template <typename VT>
    inline std::vector< std::vector < VT > > get_matrix_variable_all(const std::vector<VT> &variable) {
        auto lil_variable = std::vector< std::vector < VT > >();

        if (row_major) {
            for(IT r = 0; r < post_ranks_.size(); r++) {
                auto beg = variable.begin() + r*maxnzr_;
                auto end = variable.begin() + r*maxnzr_ + rl_[r];
                lil_variable.push_back(std::vector<VT>(beg, end));
            }
        } else {
            std::cerr << "ELLMatrix::get_matrix_variable_all() is not implemented for column major" << std::endl;
        }
        return lil_variable;
    }

    /**
     *  @brief      retrieve a specific row from the given variable.
     *  @details    this function is only called by the Python interface to retrieve the current value of a *local* variable.
     *  @tparam     VT          data type of the variable.
     *  @param[in]  lil_idx     index of the selected row. To get the correct index use the post_rank array, e. g. lil_idx = post_ranks.find(row_idx).
     *  @returns    a vector containing all elements of the provided variable and lil_idx
     */
    template <typename VT>
    inline std::vector< VT > get_matrix_variable_row(const std::vector< VT >& variable, const IT &lil_idx) {
        assert( (lil_idx < post_ranks_.size()) );
        assert( (lil_idx < rl_.size()) );

        if (row_major) {
            auto beg = variable.begin() + lil_idx*maxnzr_;
            auto end = variable.begin() + lil_idx*maxnzr_ + rl_[lil_idx];

            return std::vector < VT >(beg, end);
        } else {
            auto tmp = std::vector < VT >(rl_[lil_idx]);
            int num_rows = post_ranks_.size();
            for (int c = 0; c < rl_[lil_idx]; c++) {
                tmp[c] = variable[c*num_rows+lil_idx];
            }
            return tmp;
        }
    }

    /**
     *  @brief      retruns a single value from the given variable.
     *  @details    this function is only called by the Python interface retrieve the current value of a *local* variable.
     *  @tparam     VT          data type of the variable.
     *  @param[in]  lil_idx     index of the selected row. To get the correct index use the post_rank array, e. g. lil_idx = post_ranks.find(row_idx).
     *  @param[in]  col_idx     index of the selected column.
     *  @returns    the value at position (lil_idx, col_idx)
     */
    template <typename VT>
    inline VT get_matrix_variable(const std::vector<VT>& variable, const IT &lil_idx, const IT &col_idx) {
        std::cerr << "ELLMatrix::get_matrix_variable() is not implemented" << std::endl;
        return static_cast<VT>(0.0); // should not happen
    }

    /**
     *  @brief      computes the size in bytes
     *  @details    contains also the required size of LILMatrix partition but not account allocated variables.
     *  @returns    size in bytes for stored connectivity
     *  @see        LILMatrix::size_in_bytes()
     */
    size_t size_in_bytes() {
        size_t size = 3 * sizeof(IT);

        size += sizeof(std::vector<IT>);
        size += post_ranks_.capacity() * sizeof(IT);

        size += sizeof(std::vector<IT>);
        size += col_idx_.capacity() * sizeof(IT);

        size += sizeof(std::vector<IT>);
        size += rl_.capacity() * sizeof(IT);

        return size;
    }

    void print_matrix_statistics() {
        size_t sum = 0;
        IT num_rows_with_nonzeros = 0;
        for (auto it = rl_.begin(); it != rl_.end(); it++ ) {
            if (*it > 0) {
                sum += *it;
                num_rows_with_nonzeros ++;
            }
        } 
        double avg_nnz_per_row = static_cast<double>(sum) / static_cast<double>(num_rows_with_nonzeros);

        std::cout << "  #rows: " << static_cast<unsigned long>(num_rows_) << std::endl;
        std::cout << "  #columns: " << static_cast<unsigned long>(num_columns_) << std::endl;
        std::cout << "  #nnz: " << nb_synapses() << std::endl;
        std::cout << "  empty rows: " << num_rows_ - num_rows_with_nonzeros << std::endl;
        std::cout << "  avg_nnz_per_row: " << avg_nnz_per_row << std::endl;
        std::cout << "  dense matrix = (" << static_cast<unsigned long>(num_rows_) << ", " <<  static_cast<unsigned long>(maxnzr_) << ")" <<\
                     " stored as " << ((row_major) ? "row_major" : "column_major") << std::endl;
    }

    /**
     *  @brief      print the matrix representation to console.
     *  @details    All important fields are printed. Please note, that type casts are
     *              required to print-out the numbers encoded in unsigned char as numbers. 
     */
    virtual void print_data_representation() {
        std::cout << "ELLMatrix instance at " << this << std::endl;
        print_matrix_statistics();

        std::cout << "  post_ranks = [ " << std::endl;
        for (IT r = 0; r < post_ranks_.size(); r++ ) {
            std::cout << static_cast<unsigned long>(post_ranks_[r]) << " ";
        }
        std::cout << "]" << std::endl;

        std::cout << "  column_indices = [ " << std::endl;
        for (IT r = 0; r < post_ranks_.size(); r++ ) {
            std::cout << "[ ";
            for( IT c = 0; c < maxnzr_; c++) {
                std::cout << static_cast<unsigned long>(col_idx_[r*maxnzr_+c]) << " ";
            }
            std::cout << "]," << std::endl;
        }
        std::cout << "]" << std::endl;
    }

};
