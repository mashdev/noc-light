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
      <div class="btn-area left">
        <a class="waves-effect waves-light btn-flat check-url-btn" v-show="submitBtn" v-on:click="separateAndTest(), showInsertButton()"> Check URL
        </a>

        <a class="waves-effect waves-red btn-flat" v-show="resetBtn" v-on:click="clearResults()">    clear
        </a>
      </div>

    <!-- <form action=""> -->
      <table class="url-tbl highlight">
        <tbody
          v-for="(get, index) in reformatted"
          v-bind:key="index"
        >
          <div class="tbl-row">
            <tr v-if="get.statuscode < 215">
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
              <td>
                <SelectMenu></SelectMenu>
              </td>
            </tr>
          </div>
        </tbody>
          <tr v-if="insertBtn">
            <td class="insert-btn-row-td center" colspan="4"> 
              <button class="btn insert-btn" v-on:click="submitEndPointUrls()">
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
    <!-- </form> -->
  </div>
  </div>
</template>

<script>
import Icons from '@/components/Icons'
import SelectMenu from '@/components/SelectMenu'

export default {
  components: {
    Icons,
    SelectMenu
  },
  data() {
    return {
      urltext : null,
      separated: [],
      urlsTotal: null,
      reformatted: [],
      failures: [],
      baseUrl: 'http://127.0.0.1:5000',
      url: 'http://localhost:5000/check/?param=',
      submitBtn : false,
      resetBtn : false,
      insertBtn : false,
      selected: ''
    }
  },

  methods: {
    separateAndTest() {
      this.separated = this.urltext.split(',');
      this.urlsTotal = this.separated.length;
      let res = this.reformatted;
      let fails = this.failures;

      fails.length = 0;
      res.length = 0;

      for(let i=0; i < this.urlsTotal; i++){
        try {
          axios.get( this.url + this.separated[i] )
          .then(function(response) {
            // console.dir(response)

            if(response.data.statuscode == 200){
              console.log("API Call Successful")
              res.push(response.data);
            }
            else if (response.data.statuscode > 300){
              console.log("API CALL FAILED: "+ response.data.statuscode);
              fails.push(response.data)
            }
          })
          .catch(function(errs) {
            fails.push("response.data failed: "+ errs);
          })
        } catch (error) {
          console.log("An error occurred: "+error);
          fails.push(response.data)
        }
      } //end for loop


      
    },

    ckSubmitBtn() {
      if(this.urltext.length > 10 && this.urltext != null) {
        this.submitBtn = true;
        this.resetBtn = true;
      }
      else {
        this.submitBtn = false;
        this.resetBtn = false;
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
        if(this.reformatted.length > 0) {
          this.insertBtn = true;
        }
        else {
          this.insertBtn = false;
        }
      }, 700)
    },

    submitEndPointUrls() {
        // console.log(urlArr);
        axios.post(this.baseUrl+'/create', {
          data: {
            params : this.reformatted
          }
        })
    }


  } //end methods:

} //end export default()
</script>

<style scoped>
table {
  width: 100%;
}

tr {
  width: 100%;
}

.tbl-row {
  padding-bottom: 10px;
  width: 100%;
}

td {
  padding: 5px;
  margin: 5px 0px 5px 0px;
  border-radius: 0;
}

.url-text-area{
  height: 15%;
  width: 100%;
}

.green-light {
  background-color: green;
  padding: 5px 3px 5px 3px;
}

.red-light {
  background-color: red;
  padding: 5px 3px 5px 3px;
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
  background-color: orange;
}

.insert-btn {
  background-color: green;
}



</style>