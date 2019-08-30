<template>
  <div>
    <div class="container">
      <p class="left">Add Url</p>
      <textarea 
        name="urltext" 
        id="urlstext" 
        class="url-text-area" 
        v-model="urltext" 
        placeholder="Enter comma separated list"
        cols="10" 
        rows="10"
      ></textarea>
      <div class="btn-area left">
        <a class="waves-effect waves-teal btn-flat" v-on:click="separateAndTest()"> Test </a>
      </div>
      <div class="formatted-urls">
      
        <table>
          <tbody
            v-for="(get, index) in reformatted" 
            v-bind:key="index"
            class=""
          >
            <tr>
              <td>
              {{ index+1 }}
              </td>
              <td>
                URL: {{ get.url }}
              </td>
              <td>
                Response Time: {{ get.calltime }}
              </td>
              <td>
                Status Code: {{ get.body }} -- Success
              </td>
            </tr>
          </tbody>
        </table>

        <!-- <table>
          <tbody
            v-for="(get, index) in failed" 
            v-bind:key="index"
            class=""
          >
            <tr>
              <td>
              {{ index+1 }}
              </td>
              <td>
                URL: {{ get.url }}
              </td>
              <td>
                Response Time: {{ get.calltime }}
              </td>
              <td>
                Status Code: {{ get.body }} -- Success
              </td>
            </tr>
          </tbody>
        </table> -->

{{ failed }}


        <p> {{ urlsTotal }} </p>
        
      </div>
    </div>



  </div>
</template>

<script>
import Icons from '@/components/Icons'

export default {
  components: {
    Icons
  },
  data() {
    return {
      urltext : null,
      separated: [],
      urlsTotal: null,
      reformatted: [],
      failed: [],
      icon: 'add',
      url: 'http://localhost:5000/check/?param='
    }
  },

  methods: {
    separateAndTest() {
      this.separated = this.urltext.split(',');
      this.urlsTotal = this.separated.length;
      let res = this.reformatted
      let failed = this.failed
      
      res.length = 0;

      for(let i=0; i < this.urlsTotal; i++){
        axios.get( this.url + this.separated[i] )
          .then(function(response) {
            res.push(response.data);
            
          })
          .catch(function(errs) {
            failed.push(errs.data);
        })
      }

      // for(let i=0; i < this.urlsTotal; i++){
      //   setInterval(function(){
      //     console.log("sleeping for half second")  
      //   },1000)
      // }
            // this.reformatted.push(this.separated[i])
          
        
        // return axios.get(url + this.separated[i])
        // .then(function(res) {
        //   // console.log(res.status)

        //   if(res.status === 200) {
        //     console.log("Success: ", res)
        //     this.reformatted.push( this.separated[i] + res.status)
        //   }
        //   else {
        //     console.log("Call to the API Failed, please adjust endpoint and try again.")
        //     this.reformatted.push( "FAILED ",this.separated[i] )
        //   }
        // })
        // .catch(function(err) {
        //   console.log("SOMETHING JUST BROKE!!: ", err, this.separated[i]);
        // })
    

      
        
    },

    testUrl(id) {
 
    },


  },

  computed: {

  }
  
}
</script>

<style scoped>
  .url-text-area{
    height: 15%;
    width: 100%;
  }
</style>