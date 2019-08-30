<template>
  <div class="container">
    <h3>NOC Light Urls</h3>
        <table class="table table-sm">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">API Endpoint</th>
              <th scope="col">URL Type</th>
              <th scope="col">Enabled</th>
            </tr>
          </thead>
          <tbody v-for="url in urls" v-bind:key="url[0]" class="">
            <tr>
              <td>
                <!-- <button 
                  type="button"
                  class="btn btn-info btn-edit"
                  data-toggle="modal"
                  data-target="updateModal"
                  v-on:click="updateUrl(1)"
                > -->
                  <!-- <modal-update :uid="id" > </modal-update> -->
                  <!-- <span class="badge badge-info"> {{ url[0] }} </span> -->
                  <!-- </a> -->
                <!-- </button> -->
                
                <button
                  type="button"
                  class="btn"
                  @click="showModal"
                >
                  Edit
                </button>

                <modal
                  v-show="isModalVisible"
                  @close="closeModal"
                  v-bind:uid="url[0]"
                />

              </td>
              <td> {{ url[1] }} </td>
              <td> {{ url[2] }} </td>
              <td> {{ url[3] }} </td>
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
      isModalVisible: false
    }
  },

  methods: {
    dashboard() {
      return axios.get("http://localhost:5000/dashboard")
      .then(res => {
        this.urls = res.data
      })
      .catch(error => {
        console.log(error)
      })
    },

  
  }, //end methods:

  computed: {

  },

  created() {
    this.dashboard()
  
  }, //end created()
}
</script>

<style scoped>

.btn-edit {
  padding: 0px 2px 0px 2px;
}

</style>
