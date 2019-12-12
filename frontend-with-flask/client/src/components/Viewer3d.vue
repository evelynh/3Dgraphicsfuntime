<template>
<div>
    <v-btn class="my-4" block> COLOUR </v-btn>
    <v-color-picker
      v-model="color"
      :hide-canvas="true"
      :hide-inputs="true"
      :hide-mode-switch="true"
      :mode.sync="mode"
      :show-swatches="false"
      @change="changeColor($event)"
      class="mx-auto"
    ></v-color-picker>

 <!-- <div id="viewer"> -->
    <model-obj 
    :backgroundColor="bgColor"
    :backgroundAlpha="bgAlpha"
    src="windmill.obj">
    </model-obj>
<!-- </div> -->
<div>
</div>
  </div>
</template>
<script>
import { ModelObj } from 'vue-3d-model';
export default {
  components: { ModelObj },
  data () {
    return {
        bgColor: 'black',
        bgAlpha: 0.5
    }
    },
    methods: {
        changeColor(value) {
            this.bgColor = value;
            window.console.log(this.bgColor);
        }
    }
}
</script>

<style>
#viewer{
    width: "75%";
    /* border: solid 2px black; */
    /* background-color: aquamarine; */
}
</style>
