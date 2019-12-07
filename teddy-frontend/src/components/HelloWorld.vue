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
       <!-- <v-btn class="my-4" block>
          Undo
          <v-icon right>mdi-undo</v-icon> 
       </v-btn>
       <v-btn class="my-4" block> 
         Redo
         <v-icon right>mdi-redo</v-icon> 
       </v-btn>
       <v-btn class="my-4" block
        @click="eraseIt"> 
         Erase
         <v-icon right>mdi-eraser</v-icon> 
       </v-btn> -->
       
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
     <!-- Canvas -->
     <!-- <v-card>
       style="{
                'border' : '1px black solid',
                'fill': 'black'
              }"
     </v-card> -->
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
      // types: ['hex', 'hexa', 'rgba', 'hsla', 'hsva'],
      type: 'hex',
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
      // curr_stroke: {
      //   txy: [],
      //   color: '#FF00FF', // NEED TO CHANGE LATER
      //   opacity: 1,
      //   width: 3
      // },
      // current_color: '#FF00FF', 
      mouseUp: false,
      mouseDown: false,
      prevX: 0,
      prevY: 0,
      mouseX: 0,
      mouseY: 0,
      slider: 5
    }),
    methods: {
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

          // create a new path
          // this.pathString = 'M' + x + ', ' + y + 'L' + (x + 1)+ ',' + (y + 1);
          this.pathString = 'M' + x + ', ' + y + ' l0, 0';

          this.strokes.push([x, y]);
          // add a newPath to
          this.newPath = this.paper.path(this.pathString);

          // this.newPath.attr({fill: this.hex});
          // window.console.log("newPath");
          // window.console.log(this.newPath);

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
      

          // window.console.log("mousex" + newx)
          // window.console.log("mousey" + newy)
          // window.console.log("prevx" + this.prevX)
          // window.console.log("prevy" + this.prevY)

          this.pathString+=('l' + (newx - this.prevX) + ',' + (newy - this.prevY));
          // this.pathString+=('L' + newx + ',  ' + newy);          
          
          // this.pathString+=('\xa0\xa0 l' + newx  + '\xa0, \xa0 ' + newy);

          // window.console.log("New path")
          // window.console.log(this.newPath);

          // this.pathString.concat('\xa0\xa0 l' + (newx - this.prevX) + '\xa0 \xa0 ' + (newy - this.prevY));
          // this.newpath.attrs.path("path", this.pathString);

          // this.newpath.attr('path', this.pathString);

          // this.newPath.attrs.path = this.pathString;
          this.newPath = this.paper.path(this.pathString);

          this.newPath.attr({
            'stroke': this.hex,
            'stroke-width': this.stroke_width
          });
          // this.newPath.attr({fill: this.hex});
          // this.newPath.attr({stroke: this.hex});

          // this.newPath.attr('path', this.pathString);
        }

        // testing out 

        // let x = this.round_float(this.mouseX);
        // let y = this.round_float(this.mouseY);

        // let newcircle = this.paper.circle(x, y, this.stroke_width);
        // newcircle.attr({fill: this.hex});
        // newcircle.attr({stroke: this.hex});


        // window.console.log("Creating a circle");
        // window.console.log(newcircle);
        // window.console.log(this.paper);

        // add stroke to the current stroke

        // this.curr_stroke.txy.push(
        //   // log the date--> helpful for debugging
        //   Date.now(),
        //   this.round_float(x/this.size_ratio),
        //   this.round_float(y/this.size_ratio)          
        // )
        
        // // initialize the path for the stroke
        // this.curr_path_string = "M" + x + "," + y;
        // this.curr_path = this.paper.path(this.curr_path_string);

        // this.curr_path.attr({
        //   stroke: this.colors.hex,
        //   "stroke-linecap": "round",
        //   "stroke-linejoin": "round",
        //   "stroke-width": this.round_float(
        //     this.stroke_width * this.size_ratio
        //   )
        //   // "stroke-opacity": this.colors.a
        // });

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
      this.size_ratio = this.card_width / 800;
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

            // this.mouseIsDown = true;

            this.drawit();

            // // print(this.mouseY);
            // window.console.log(this.mouseX);
            // window.console.log(this.mouseY);

            //  this.$refs.canvas.addEventListener("mousemove", ()=> {
            //   window.console.log("MOVEMENT")
            //   this.prevX = this.mouseX;
            //   this.prevY = this.mouseY;
            //   this.mouseX = e.offsetX;
            //   this.mouseY = e.offsetY;

            //   // let newcircle = this.paper.circle(this.mouseX, this.mouseY, 50);
            //   // newcircle.attr({fill: "blue"});
            //   // newcircle.attr({stroke: "black"});
            //   this.drawit();
            // });
            // alert(this.mouseX);
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

              // let newcircle = this.paper.circle(this.mouseX, this.mouseY, 5);
              // newcircle.attr({fill: "blue"});
              // newcircle.attr({stroke: "blue"});
              // this.drawit();
            });
        // this.$refs.canvas.addEventListener("mousemove", ()=> {
        //   window.console.log("MOVEMENT")
        //   this.drawit();
        // });

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

          // this.newPath.attr({fill: this.hex});
          // window.console.log("newPath");
          // window.console.log(this.newPath);

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
