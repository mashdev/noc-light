<template>
  <div class="container">
    <h3>NOC Light Urls</h3>
        <table class="table table-sm">
          <thead>
            <tr class="text-left">
              <th scope="col">API Endpoint</th>
              <th scope="col">URL Type</th>
              <th scope="col">Enabled</th>
              <th scope="col">Update</th>
            </tr>
          </thead>
          <tbody v-for="url in urls" v-bind:key="url[0]" class="text-left">
            <tr>
              <td> {{ url[1] }} </td>
              <td> {{ url[2] }} </td>
              <td> {{ url[3] }} </td>
              <td>
                <a v-bind:href="/update/+url[0]"
                >
                  <span class="btn btn-outline-dark">Edit</span>
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
      urls: null,
      dash: '',
      isModalVisible: false,
    };
  },

  methods: {
    dashboard() {
      return axios.get('http://localhost:5000/dashboard')
        .then((res) => {
          this.urls = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },


  }, // end methods:

  computed: {

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

</style>
