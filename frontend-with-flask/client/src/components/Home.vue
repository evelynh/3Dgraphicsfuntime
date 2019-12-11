<template>
  <v-container
    fluid
  >
    <!-- Layout for the entire project row 1 -->
    <v-layout
      align-center 
      justify-center
      text-center
      wrap
    >
    <!-- Layout for the  column on the left (for buttons-->
     <v-layout column align-center justify-space-around fill-height>
         <p>{{ msg }}</p>
       <v-btn class="my-4" block
        @click="drawPressed"> 
         Draw
         <v-icon right>mdi-draw</v-icon> 
       </v-btn>
       <v-btn class="my-4" block
        @click="clearIt"> 
         Clear
         <v-icon right>mdi-autorenew</v-icon> 
       </v-btn>
       <v-btn class="my-4" block> 
         Submit
         <v-icon right>mdi-upload</v-icon> 
       </v-btn>
     </v-layout>
     <v-spacer></v-spacer>
      <v-card class="elevation-12" :width="card_width" :height="card_height">
            <div id="canvas"
              ref="canvas"
              :width="card_width" 
              :height="card_height"
              style="border: 1px black solid"
            ></div>
      </v-card>
     <v-layout column align-center justify-space-between fill-height>
       <v-row>
          <v-col
            class="justify-center"
          >
          <v-row>
            <v-color-picker 
              v-model="color" 
              show-swatches
              @change="changeColor($event)">
            </v-color-picker>
          </v-row>
          <v-spacer></v-spacer>
          <v-row>
            <v-slider
              min="3"
              max="75"
              id="brushSize"
              @change="changeBrushSize($event)"
              label="Select Brush Size"
              v-model="slider"
              thumb-label>
            </v-slider>
          </v-row>
          </v-col>
        </v-row>
      </v-layout>
    </v-layout>
    <v-layout>
      <Viewer3d/>
    </v-layout>

  </v-container>
</template>

<script>
import Raphael from "raphael";
import axios from 'axios';
import Viewer3d from './Viewer3d';

// import VueColor from "vue-color";

  export default {
    name: 'Home',
    components: {
      Viewer3d,
    },
    data: () => ({
      // types: ['hex', 'hexa', 'rgba', 'hsla', 'hsva'],
      type: 'hex',
      msg: '',
      hex: '#FF00FF',
      // hexa: '#FF00FFFF',
      counter: 0,
      rgba: { r: 255, g: 0, b: 255, a: 1 },
      hsla: { h: 300, s: 1, l: 0.5, a: 1 },
      hsva: { h: 300, s: 1, v: 1, a: 1 },
      card_width: 500,
      card_height: 500,
      newPath: undefined,
      pathString:"",
      stroke_width: 5,
      size_ratio: 0,
      colors: { a: 1, hex: "#000000" },
      // eraser_mode: false,
      // drawing_mode: false,
      is_outside_canvas: false,
      // is_drawing: false,
      // is_inside_canvas: false,
      strokes: [],
      paper: undefined,
      first: false,
      mouseUp: false,
      mouseDown: false,
      prevX: 0,
      prevY: 0,
      mouseX: 0,
      mouseY: 0,
      slider: 5
    }),
    methods: {
        getMessage() {
        const path = 'http://localhost:5000/';
        axios.get(path)
            .then((res) => {
            this.msg = res.data;
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
        },
      round_float(f) {
        return Number(parseFloat(f).toFixed(2));
      },
      changeBrushSize(value){
        this.stroke_width = value;
      },
      changeColor(value){
        this.hex = value;
      },
      eraseIt(){
        // this is currently a placeholder, and I'm going to have to change it later
        this.hex = "#ffffff";
      },
      drawPressed(){
        this.hex = '#FF00FF';
      },
      clearIt(){
        // note, this will all have to change later with new implementation of strokes
        window.console.log("Clearing!")
        let currCanvas = document.getElementById("canvas");
        currCanvas.innerHTML = "";
        this.strokes=[]
        this.pathString = ""
        this.paper = new Raphael(
        this.$refs.canvas,
        this.card_width,
        this.card_height
      );
      },
      drawit(){
        // capture that drawing inside of canvas
        // this.is_drawing = true;
        this.is_outside_canvas = false;

        // var finalPath = newPath;

        if(this.first == true)
        {
          // clear canvas, making it limited to only one stroke
          this.clearIt();
          // set x and y values
          let x = this.round_float(this.mouseX);
          let y = this.round_float(this.mouseY);

          this.pathString = 'M' + x + ', ' + y + ' l0, 0';

          this.strokes.push([x, y]);
          // add a newPath to
          this.newPath = this.paper.path(this.pathString);


          this.newPath.attr({
            'stroke': this.hex,
            'stroke-width': this.stroke_width
          });
          

          // indicate this is no longer the first point
          this.first = false;
        }
        else
        {
          
          // set x and y
          let newx = this.round_float(this.mouseX);
          let newy = this.round_float(this.mouseY);

          // only send every 5 strokes or so--> don't want too many verticies 
          if (this.counter % 2 === 0)
          {
            // add to strokes
            this.strokes.push([newx, newy]);    
          }
          this.pathString+=('l' + (newx - this.prevX) + ',' + (newy - this.prevY));

          this.newPath = this.paper.path(this.pathString);

          this.newPath.attr({
            'stroke': this.hex,
            'stroke-width': this.stroke_width
          });
        }
      }
    },
    // after page loads, these even listeners come into play
    mounted(){
      this.size_ratio = this.card_width / 800;
      this.paper = new Raphael(
        this.$refs.canvas,
        this.card_width,
        this.card_height
      );
        this.$refs.canvas.addEventListener("mousedown", ()=>{
            this.mouseDown = false;
            this.first = true;
            this.mouseUp = true;
        });


        this.$refs.canvas.addEventListener("mousedown", (e)=>{
          // reset strokes array
          this.strokes = [];
          this.counter = 0;

          // set boleans
          this.mouseDown = false;
          this.first = true;
          this.mouseUp = true;
          // alert("Mousedown");            
            window.console.log("Current (x,y) position");
            this.mouseDown = true;
            this.mouseUp = false;
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;

            this.drawit();
        });

        this.$refs.canvas.addEventListener("mousemove", (e)=> {
              this.counter += 1;
              this.prevX = this.mouseX;
              this.prevY = this.mouseY;
              this.mouseX = e.offsetX;
              this.mouseY = e.offsetY;
              if (this.mouseDown)
              {
                window.console.log("drawing!");
                this.drawit();
              }
            });

        // check for out of canvas
        this.$refs.canvas.addEventListener("pointerleave", ()=>{
           this.pathString += 'z';

           this.newPath = this.paper.path(this.pathString);

            this.newPath.attr({
            'stroke': this.hex,
            'stroke-width': this.stroke_width
          });
          

          this.mouseDown = false;
          this.mouseUp = true;

          // return strokes
          window.console.log("Final Strokes");
          window.console.log(this.strokes);

        })

        // check for when you are up on the canvas
        this.$refs.canvas.addEventListener("mouseup", ()=>{

          this.pathString += 'z';

           this.newPath = this.paper.path(this.pathString);

          this.newPath.attr({
            'stroke': this.hex,
            'stroke-width': this.stroke_width
          });
          
          // alert("Mouseup");
          // turn off the mousedown and mouseup switch
          this.mouseDown = false;
          this.mouseUp = true;

          // return strokes
          window.console.log("Final Strokes");
          window.console.log(this.strokes);

        });
        // disable right click menu on canvas
        this.$refs.canvas.addEventListener("contextmenu", e => e.preventDefault());
      },
    computed: {
      color: {
        get () {
          return this[this.type]
        },
        set (v) {
          this[this.type] = v
        },
      },
      showColor () {
        if (typeof this.color === 'string') return this.color

        return JSON.stringify(Object.keys(this.color).reduce((color, key) => {
          color[key] = Number(this.color[key].toFixed(2))
          return color
        }, {}), null, 2)
      },
    },
    created() {
        this.getMessage();
    },
  }


// export default {
//   name: 'Ping',
//   data() {
//     return {
//       msg: '',
//     };
//   },
//   methods: {
//     getMessage() {
//       const path = 'http://localhost:5000/ping';
//       axios.get(path)
//         .then((res) => {
//           this.msg = res.data;
//         })
//         .catch((error) => {
//           // eslint-disable-next-line
//           console.error(error);
//         });
//     },
//   },
//   created() {
//     this.getMessage();
//   },
// };

</script>


