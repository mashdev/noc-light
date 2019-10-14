<template>
  <div class="container">
    <h3>NOC Light Urls</h3>
    <i class="material-icons"> {{sort ? arrowup : arrowdown }} </i>
        <table class="table table-sm">
          <thead>
            <tr class="text-left">
              <th scope="col" > 
                <span 
                  @click="sortByColumn('urlEndpoint')"
                  class="sort-by"
                > API Endpoint 
                </span>
              </th>
              <th scope="col">
                <span 
                  @click="sortByColumn('urlType')"
                  class="sort-by"
                > URL Type 
                </span>
              </th>
              <th scope="col">
                <span 
                  @click="sortByColumn('urlEnabled')"
                  class="sort-by"
                > Enabled 
                </span>
              </th>
              <th scope="col">
                Update
              </th>
            </tr>
          </thead>
          <tbody v-for="url in urls" v-bind:key="url[0]" class="text-left">
            <tr>
              <td> {{ url[1] }} </td>
              <td> {{ url[3] }} </td>
              <td> {{ url[2] == 0 ? "No" : "Yes" }} </td>
              <td>
                <a v-bind:href="/update/+url[0]"
                >
                  <span class="btn btn-outline-dark btn-sm">Edit</span>
                </a>
              </td>
            </tr>
          </tbody>
        </table>
  </div>
</template>

<script>

export default {
  components: {
  },

  data() {
    return {
      urls: '',
      dash: '',
      sort: true,
      endPointSortBy: 'ASC',
      arrowup: 'keyboard_arrow_up',
      arrowdown: 'keyboard_arrow_down'
    };
  },

  methods: {
    dashboard() {
      return axios.get('http://localhost:5000/dashboard', 
      {
        params: {
          column: 'null',
          sortBy: 'null'
        },
      })
        .then((res) => {
          console.log(res.data[0]);
          this.urls = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    sortByColumn(col) {
      this.sort = !this.sort;

      if (this.sort) {
        this.endPointSortBy = 'ASC';
        this.getRequestDash(col, this.endPointSortBy);
      } 
      else if (!this.sort) {
        this.endPointSortBy = 'DESC';
        this.getRequestDash(col, this.endPointSortBy);
      }
    },

    sortByUrlType(col) {
      this.sort = !this.sort;

      if (this.sort) {
        this.endPointSortBy = 'ASC';
        this.getRequestDash(col, this.endPointSortBy);
      } 
      else if (!this.sort) {
        this.endPointSortBy = 'DESC';
        this.getRequestDash(col, this.endPointSortBy);
      }
    },

    getRequestDash(endpoint, filter) {
      return axios.get('http://localhost:5000/dashboard', {
        params: {
          column: endpoint,
          sortBy: filter,
        },
      })
        .then((res) => {
          // console.log(res.data);
          this.urls = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },


  }, // end methods:

  computed: {
    testComp() {
      alert('Computed Ran');
    },
  },

  created() {
    this.dashboard();
  }, // end created()
};
</script>

<style scoped>

.btn-edit {
  padding: 0px 2px 0px 2px;
}

.sort-by {
  text-decoration:underline;
  cursor: pointer;
}

</style>
