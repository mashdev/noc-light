<template>
  <div class="container">

    <div class="">
      <h3>Edit Endpoint Update</h3>
      </div>

      <div
        v-for="(result, id) in urlsArr[0]"
        v-bind:key="id"
        class="row"
      >
        <div class="col-md-6 text-left">
          <span class=""> Endpoint </span>
            <input
              type="text"
              class="form-control"
              id="endpoint-url"

              v-model="urlEndpointCheck"
            >
        </div>
        <div class="col-md-3 text-left">
          Url Type:
          <div>
            <select
              name=""
              id=""
              class="form-control"
              v-model="urlType"
            >
              <option
                v-for="(result2, id2) in urlsArr[1]"
                v-bind:key="id2"
                :value="result2.catid"
              >
                {{ result2.categoryName }}
              </option>
            </select>
          </div>

        </div>

        <div class="col-md-3 text-left">
          Is Enabled:
          <select
            name=""
            id=""
            class="form-control"
            v-model="isEnabled"
            v-on:change="selectIsEnabled($event)"
          >

            <option
              v-for="(val, index) in enabledList"
              v-bind:key="index"
              :value="val.id"
            >
              {{ val.name }}
            </option>

          </select>
        </div>

        <button
          class="btn btn-warning submit-btn"
          @click="checkUrlAndSubmit(urlEndpointCheck, urlId)"
        >
          Submit
        </button>
        <button
          class="btn btn-secondary submit-btn"
          v-on:click="cancelUpdate"
        >
        Cancel
        </button>
      </div>


  </div>
</template>

<script>

export default {
  components: {},

  data() {
    return {
      urlId: this.$route.params.id,
      urlsArr: '',
      enabledList: [
        { name: 'Disabled', id: 0 },
        { name: 'Enabled', id: 1 },
      ],
      isEnabled: '',
      urlType: '',
      urlEndpoint: '',
      urlEndpointCheck: '',
      urlCategories: [],
      checkUrl: 'http://localhost:5000/check/?param=',
    };
  },

  methods: {
    updateById(id) {
      return axios.get(`http://localhost:5000/update/${id}`)
        .then((response) => {
          this.urlsArr = response.data;
          this.urlCategories = response.data.categories;
          this.urlType = response.data[0][0].catid;
          this.isEnabled = response.data[0][0].urlEnabled;
          this.urlEndpointCheck = response.data[0][0].urlEndpoint;
          this.idForUpdate = response.data[0][0].id;
        })
        .catch((error) => {
          console.log(error);
          alert(error)
        });
    },

    selectIsEnabled(event) {
      this.isEnabled = event.target.value;
      console.log(event.target.value);
    },

    checkUrlAndSubmit(url, urlId) {
      this.urlEndpointCheck;

      return axios.get(`http://localhost:5000/check/?param=${url}`)
        .then((response) => {
          try {
            if (response.data.statuscode == 200) {
              axios.post(`http://localhost:5000/update/${urlId}`, {
                data: {
                  params: {
                    endpoint: this.urlEndpointCheck,
                    urltype: this.urlType,
                    isenabled: this.isEnabled,
                    uid: this.urlId,
                  },
                  headers: {
                    'Content-Type': 'application/json',
                  },
                },
              })
                .then((response) => {
                  console.log(response);

                  if (response.status == 204) {
                    alert('No changes detected');
                    this.$router.push('/dashboard');
                  } else if (response.status == 200) {
                    alert('Endpoint successfully updated.');
                    this.$router.push('/dashboard');
                  }
                })
                .catch((error) => {
                  console.log(error);
                  alert(error);
                });

              // console.log(this.urlEndpointCheck+" "+this.urlType+" "+this.isEnabled )
              // axios.post(`http://localhost:5000/update/${url}`)
            } else if (response.data.statuscode >= 400) {
              console.log(response.data);
              alert(response.data.text);
            }
          } catch (error) {
            console.log(error);
          }
        });
    },

    cancelUpdate() {
      this.$router.push('/dashboard');
    },

  },

  mounted() {
    this.updateById(this.urlId);
  },


};
</script>

<style scoped>

.submit-btn {
  margin: 10px 15px;
}

</style>
