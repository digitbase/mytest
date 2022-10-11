<template>
  <div v-on:click="dodo">
    <button v-on:click.stop="doThis">阻止单击事件继续传播</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      class_1: 'box',
      classArr: ['', 'box_green', ''],
      classObj: {
        box_black: false,
        box_red: true,
      },
    }
  },
  methods: {
    doThis: function () {
      alert('noclick')
    },
    dodo: function () {
      alert('dodo')
    },
  },
}
</script>

<style lang="scss" scoped>
.select {
  margin-top: 20px;
  margin-bottom: 20px;
  overflow: hidden;
  /* color:white; */
}

.box {
  float: left;
  height: 80px;
  width: 80px;
  background-color: rgb(255, 255, 255);
  margin-left: 20px;
  line-height: 70px;
  text-align: center;
  border-radius: 10px;
  border: 1px rgb(212, 211, 211) solid;
  /* font-size: 20px; */
}

.box_green {
  float: left;
  height: 80px;
  width: 80px;
  background-color: rgb(4, 112, 49);
  margin-left: 20px;
  line-height: 70px;
  text-align: center;
  border-radius: 10px;
  border: 1px rgb(212, 211, 211) solid;
  color: white;
  /* font-size: 20px; */
}

.box_black {
  float: left;
  height: 80px;
  width: 80px;
  background-color: rgb(0, 0, 0);
  margin-left: 20px;
  line-height: 70px;
  text-align: center;
  border-radius: 10px;
  border: 1px rgb(248, 2, 2) solid;
  color: white;
}

.box_red {
  float: left;
  height: 80px;
  width: 80px;
  background-color: rgb(251, 0, 0);
  margin-left: 20px;
  line-height: 70px;
  text-align: center;
  border-radius: 10px;
  border: 1px rgb(248, 2, 2) solid;
  color: white;
}

button {
  margin-top: 30px;
  margin-left: 40px;
  width: 220px;
  height: 60px;
  border-radius: 10px;
  background-color: rgb(9, 79, 170);
  color: antiquewhite;
  font-size: 20px;
}
</style>
