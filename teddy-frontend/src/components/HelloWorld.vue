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
       <v-btn class="my-4" block>
          Undo
          <v-icon right>mdi-undo</v-icon> 
       </v-btn>
       <v-btn class="my-4" block> 
         Redo
         <v-icon right>mdi-redo</v-icon> 
       </v-btn>
       <v-btn class="my-4" block> 
         Erase
         <v-icon right>mdi-eraser</v-icon> 
       </v-btn>
       
       <v-btn class="my-4" block> 
         Draw
         <v-icon right>mdi-draw</v-icon> 
       </v-btn>
       <v-btn class="my-4" block> 
         Clear
         <v-icon right>mdi-autorenew</v-icon> 
       </v-btn>
       <v-btn class="my-4" block> 
         Submit
         <v-icon right>mdi-upload</v-icon> 
       </v-btn>
     </v-layout>
     <v-spacer></v-spacer>
     <!-- Canvas -->
     <!-- <v-card>
     </v-card> -->
      <v-card class="elevation-12" :width="card_width" :height="card_height">
            <canvas id="canvas"
              ref="canvas"
              :width="card_width" 
              :height="card_height"
              style="border: 1px black solid"
            ></canvas>
      </v-card>
     <v-layout column align-center justify-space-between fill-height>
       <v-row>
          <!-- <v-col
            cols="12"
            md="4"
          >
            <v-btn
              v-for="t in types"
              :key="t"
              class="my-4"
              block
              @click="type = t"
            >{{ t }}</v-btn>
          </v-col> -->
          <!-- <v-col
            class="d-flex justify-center"
          >

          </v-col> -->
          <v-col
            class="justify-center"
          >
          <v-row>
            <v-color-picker v-model="color" show-swatches></v-color-picker>
          </v-row>
          <v-spacer></v-spacer>
          <v-row>
            <v-slider
              min="5"
              max="50"
              label="Select Brush Size"
              v-model="slider"
              thumb-label>
            </v-slider>
          </v-row>
          </v-col>
          <!-- <v-col
            cols="12"
            md="4"
          >
            <v-sheet
              dark
              class="pa-4"
            >
              <pre>{{ showColor }}</pre>
            </v-sheet>
            
          </v-col> -->
          <!-- <v-col>
            
          </v-col> -->
        </v-row>
      </v-layout>
    </v-layout>
    <!-- <v-layout
      align-center 
      justify-center
      wrap
    >
    <v-row>
      <v-col>
        <h3 >
          Options
        </h3>
      <v-slider
      min="5"
      max="50"
      label="Select Brush Size"
      v-model="slider"
      thumb-label>
      </v-slider>
      </v-col>
      <v-col>
      </v-col>
    </v-row>
    </v-layout> -->
  </v-container>
</template>

<script>
import Raphael from "raphael";
// import VueColor from "vue-color";

  export default {
    data: () => ({
      types: ['hex', 'hexa', 'rgba', 'hsla', 'hsva'],
      type: 'hex',
      hex: '#FF00FF',
      hexa: '#FF00FFFF',
      rgba: { r: 255, g: 0, b: 255, a: 1 },
      hsla: { h: 300, s: 1, l: 0.5, a: 1 },
      hsva: { h: 300, s: 1, v: 1, a: 1 },
      card_width: 500,
      card_height: 500,
      eraser_mode: false,
      drawing_mode: false,
      is_outside_canvas: false,
      is_inside_canvas: false,
      strokes: [],
      paper: undefined,
      redo_strokes: [],
      eraser_strokes: [],
      current_color: '#FF00FF', // NEED TO GET COLOR FROM COLOR PICKER SOMEHOW
      mouseUp: false,
      mouseDown: false,
      prevX: 0,
      prevY: 0,
      mouseX: 0,
      mouseY: 0,
      slider: 20
    }),
    methods: {
      drawit(){
        let newcircle = this.paper.circle(100, 35, 25);
        newcircle.attr({fill: "blue"});

        window.console.log(newcircle);
        window.console.log(this.paper);
        
        // get the canvas to draw on
        // let context = document.getElementById("canvas");
        // context.beginPath();
        // context.strokeStyle = this.current_color;
        // context.lineWidth = 4;
        // context.moveTo(this.prevX, this.prevY);
        // context.lineTo(this.mouseX, this.mouseY);
        // context.stroke();
      }
    },
    // after page loads, these even listeners come into play
    mounted(){
      this.paper = new Raphael(
        this.$refs.canvas,
        this.card_width,
        this.card_height
      );
    //   for(var i = 0; i < 5; i+=1) {
    //     var multiplier = i*5;
    //     this.paper.circle(250 + (2*multiplier), 100 + multiplier, 50 - multiplier)
    // }
        // this.$refs.canvas;
        // let theCanvas = this.document.getElementById('cavnas');
        // let theCanvas = document.getElementById('cavnas');

        // theCanvas.addEventListener("mousedown", (e)=>{
            
        //     window.console.log("hello");
        //     this.mouseDown = true;
        //     this.mouseX = e.offsetX;
        //     this.mouseY = e.offsetY;
        //     // print(this.mouseY);
        //     window.console.log(this.mouseX);
        //     window.console.log(this.mouseY);
        //     })

        // this.$refs.addEventListener("mousedown", (e)=>{
            
        //     window.console.log("hello");
        //     this.mouseDown = true;
        //     this.mouseX = e.offsetX;
        //     this.mouseY = e.offsetY;
        //     // print(this.mouseY);
        //     window.console.log(this.mouseX);
        //     window.console.log(this.mouseY);
        // })
        this.$refs.canvas.addEventListener("mousedown", (e)=>{
          // alert("Mousedown");            
            window.console.log("Current (x,y) position");
            this.mouseDown = true;
            this.mouseUp = false;
            this.prevX = this.mouseX;
            this.prevY = this.mouseY;
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;
            // print(this.mouseY);
            window.console.log(this.mouseX);
            window.console.log(this.mouseY);

             this.$refs.canvas.addEventListener("mousemove", ()=> {
              window.console.log("MOVEMENT")
              this.prevX = this.mouseX;
              this.prevY = this.mouseY;
              this.mouseX = e.offsetX;
              this.mouseY = e.offsetY;
              this.drawit();
            });
            // alert(this.mouseX);
        });
        // this.$refs.canvas.addEventListener("mousemove", ()=> {
        //   window.console.log("MOVEMENT")
        //   this.drawit();
        // });
        this.$refs.canvas.addEventListener("mouseup", ()=>{
          // alert("Mouseup");
          // turn off the mousedown and mouseup switch
          this.mouseDown = false;
          this.mouseUp = true;

        });
        // disable right click menu on canvas
        this.$refs.canvas.addEventListener("contextmenu", e => e.preventDefault());
        // this.$refs.canvas.addEventListener("pointerdown", this.pointerdown);
        // this.$refs.canvas.addEventListener("pointermove", this.pointermove);
        // document.addEventListener("pointerup", this.pointerup);

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
  }
</script>
