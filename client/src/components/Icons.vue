<template>
  <div>

    <i class="material-icons" v-on:click="check(uid)">
      {{ iconshape }}
    </i>

    <i v-if="iconshape == check" class="material-icons" >
      {{ remove }}
    </i>
    <i v-else class="material-icons" >
      {{ remove }}
    </i>


  </div>

</template>

<script>
export default {

  name: 'Icons',

  props: ['uid'],

  data() {
    return {
      iconshape: 'add',
      remove: 'close',
    };
  },

  methods: {
    check(id) {
      // alert(id)
      this.iconshape = 'check';
    },
  },

  computed: {

  },

};
</script>

<style scoped>


</style>
