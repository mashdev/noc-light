<template>
  <div>
    <div class="input-field" v-for="items in selectMenu">
      <select>
        <option value="1"> {{ items.value }} </option>
      </select>
    </div>

  </div>
</template>

<script>
export default {
  props: [
    'urltype',
  ],

  data() {
    return {

    };
  },
};
</script>

<style scoped>
  /*   */

</style>
