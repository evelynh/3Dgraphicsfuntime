<template>
<v-container>
    BACKGROUND COLOUR: 
    <div class="button-group">
        <v-btn text small color="black" @click="changeBlack">BLACK</v-btn>
        <v-btn text small color="grey" @click="changeWhite">WHITE</v-btn>
        <v-btn text small color="blue" @click="changeBlue">BLUE</v-btn>
    </div>

    <model-obj 
        :backgroundColor="bgColor"
        src="windmill.obj"
        margin= "10px"
        >
    </model-obj>
   <v-btn class="my-4" color="primary" block @click="handleBack"> GO BACK </v-btn>
    <div> POSSIBLE ACTIONS: Panning, zooming, rotating around your object! </div>
</v-container>
</template>
<script>
import { ModelObj } from 'vue-3d-model';
export default {
  components: { ModelObj },
  data () {
    return {
        bgColor: '#ADD8E6',
    }
    },
    methods: {
        handleBack() {
            window.location.href = '/';
        },
        changeBlack() {
            this.bgColor = "black";
        },
        changeWhite() {
            this.bgColor = "white";
        }, 
        changeBlue() {
            this.bgColor = "#ADD8E6";
        }
    }
}
</script>

<style>
#button-group {
    padding-bottom: 10px;
}
</style>
