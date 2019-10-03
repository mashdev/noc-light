<template>
  <div class="container">

    <div class="">
      <h3>Edit Endpoint Update</h3>
      </div>

      <div v-for="(result, id) in url" v-bind:key="id" class="row" >
        <div class="col-md-6 text-left">
          <span class=""> Endpoint </span>
          <input type="text" v-bind:value="result[1]" class="form-control">
        </div>

        <div class="col-md-3 text-left">
          Url Type:
          <select
            name=""
            id=""
            class="form-control"
            v-model="urlType"
          >
            <option value="0">0</option>
            <option value="1">1</option>
        </select>
        </div>

        <div class="col-md-3 text-left">
          Is Enabled:
          <select
            name=""
            id=""
            class="form-control"
            v-model="isEnabled"
          >
          <!-- use for loop to assign values -->
            <option value="0" selected> Disabled </option>
            <option value="1"> Enabled </option>
          </select>
        </div>

      </div>


  </div>
</template>

<script>
export default {
  components: {},

  data() {
    return {
      urlId: this.$route.params.id,
      url: '',
      isEnabled: '',
      urlType: '',
    };
  },

  methods: {
    updateById(id) {
      return axios.get(`http://localhost:5000/update/${this.urlId}`)
        .then((response) => {
          console.log(response.data);
          this.url = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  computed: {

  },

  created() {
    this.updateById();
  },
};
</script>

<style scoped>

</style>
