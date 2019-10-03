<template>
  <div>
    <div class="container">
      <p class="left slim">Enter URL Endpoint(s)</p>
      <textarea
        name="urltext"
        id="urlstext"
        class="url-text-area"
        v-model="urltext"
        v-on:keyup="ckSubmitBtn"
        v-on:mouseup="ckSubmitBtn"
        placeholder="(For multiple endpoints separate with a comma)"
        rows="10"
      ></textarea>
      <div class="btn-area text-left">
        <a class="btn btn-outline-success check-url-btn" v-show="submitBtn" v-on:click="separateAndTest(), showInsertButton()"> Check URL
        </a>
        <a class="btn btn-outline-warning" v-show="resetBtn" v-on:click="clearResults()">
          Clear
        </a>
      </div>

      <table class="table table-borderless">
        <tbody
          v-for="(get, index) in reformatted"
          v-bind:key="index"
          class="tbl-body"
        >
          <div class="">
            <tr class="tbl-row" v-if="get.statuscode < 215">
              <td class="green-light">
              </td>
              <td>
                URL: {{ get.url }}
              </td>
              <td>
                Call Time: {{ get.calltime.toFixed(2) }}
              </td>
              <td class="green-text">
                Status Code: {{ get.statuscode }}
              </td>
            </tr>
          </div>
        </tbody>
          <tr v-if="insertBtn">
            <td class="insert-btn-row-td center" colspan="4">
              <button class="btn btn-success" v-on:click="submitEndPointUrls()">
                Insert
              </button>
            </td>
          </tr>

        <tbody
          v-for="(fail, index) in failures"
          v-bind:key="index"
        >
        <div class="tbl-row">
          <tr v-if="fail.statuscode > 215">
            <td class="red-light">
            </td>
            <td>
              URL: {{ fail.url }}
            </td>
            <td>
              Call Time: N/A
            </td>
            <td class="red-text">
              Status Code: <span> {{ fail.statuscode }} </span>
            </td>
          </tr>
        </div>
        </tbody>
      </table>

    <div v-if="resultSet.length > 0">
      <div
        v-for="(result, rs) in resultSet"
        v-bind:key="rs"
      >
        <div v-if="result.stat == 800">
          <p>{{ result.url }}<span class="dupe-record"> is already saved to the database.</span> </p>
        </div>

        <div v-if="result.stat == 200">
          <p>{{ result.url }} <span class="success-entry"> successfully saved to database </span></p>
        </div>

      </div>
    </div>
  </div>
  </div>
</template>

<script>
import Icons from '@/components/Icons';
import SelectUrlType from '@/components/UrlTypeDDL';

export default {
  components: {
    Icons,
    SelectUrlType,
  },
  data() {
    return {
      urltext: null,
      separated: [],
      urlsTotal: null,
      reformatted: [],
      failures: [],
      baseUrl: 'http://127.0.0.1:5000',
      url: 'http://localhost:5000/check/?param=',
      submitBtn: false,
      resetBtn: false,
      insertBtn: false,
      selected: '',
      selectMenu: [
        { id: 1, item: 'Internal Site', value: 1 },
        { id: 2, item: 'External Site', value: 2 },
      ],
      selectedItem: [],
      resultSet: [],
    };
  },

  methods: {
    separateAndTest() {
      this.separated = this.urltext.split(',');
      this.urlsTotal = this.separated.length;
      const res = this.reformatted;
      const fails = this.failures;

      fails.length = 0;
      res.length = 0;

      for (let i = 0; i < this.urlsTotal; i++) {
        try {
          axios.get(this.url + this.separated[i])
            .then((response) => {
              if (response.data.statuscode == 200) {
                res.push(response.data);
              } else if (response.data.statuscode > 300) {
                console.log(`API CALL FAILED: ${response.data.statuscode}`);
                fails.push(response.data);
              }
            })
            .catch((errs) => {
              fails.push(`response.data failed: ${errs}`);
            });
        } catch (error) {
          console.log(`An error occurred: ${error}`);
          fails.push(response.data);
        }
      } // end for loop
    },

    ckSubmitBtn() {
      if (this.urltext != null) {
        if (this.urltext.length > 10 && this.urltext != null) {
          this.submitBtn = true;
          this.resetBtn = true;
          this.resultSet.length = 0;
        } else {
          this.submitBtn = false;
          this.resetBtn = false;
        }
      }
    },

    clearResults() {
      this.reformatted.length = 0;
      this.failures.length = 0;
      this.urltext = '';
      this.resetBtn = false;
      this.submitBtn = false;
    },

    showInsertButton() {
      setInterval(() => {
        if (this.reformatted.length > 0) {
          this.insertBtn = true;
        } else {
          this.insertBtn = false;
        }
      }, 700);
    },

    submitEndPointUrls() {
      axios.post(`${this.baseUrl}/create`, {
        data: {
          params: this.reformatted,
        },
      })
        .then((resp) => {
          for (let i = 0; i < resp.data.length; i++) {
            this.resultSet.push(resp.data[i]);
          }
          this.clearResults();
        })
        .catch((err) => {
          console.log('Error caught: ');
          console.log(err);
          this.resultSet.push(err);
        });
    },

    addSelectedUrlType(uid, items) {
      const res = this.reformatted;
      res[2].push(items);
    },


  }, // end methods:

}; // end export default()
</script>

<style scoped>
table {
  width: 100%;
}

td {
  /* width: 100%; */
  padding: 5px;
  margin: 5px 0px 5px 0px;
  border-radius: 0;
  text-align: left;
}

.tbl-body {
  width: 100%;
}

.tbl-row {
  padding-bottom: 10px;
  /* width: 100%; */
}

.url-text-area{
  height: 15%;
  width: 100%;
}

.green-light {
  background-color: green;
  padding: 5px 3px 5px 3px;
  width: 3px;
}

.red-light {
  background-color: red;
  padding: 5px 3px 5px 3px;
  width: 3px;
}

.tbl-row-err {

}

.red-text {
  color: red;
}

.green-text {
  color: green;
}

.slim {
  padding: 0px;
  margin: 0px;
}

.insert-btn-row-td {
  padding-bottom: 2%;
}

.btn-area {
  margin-bottom: 2%;
}

.check-url-btn {
  margin-right: 10px;
}

.insert-btn {
  background-color: green;
}

.dupe-record {
  color: red;
}

.success-entry {
  color: green;
}

</style>
