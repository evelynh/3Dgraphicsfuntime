<template>
  <v-container
    fluid
  >
    <!-- Layout for the entire project -->
    <v-layout
      align-center 
      justify-center
      text-center
      wrap
    >
    <!-- Layout for the  column on the left (for buttons-->
     <v-layout column align-center justify-space-around fill-height>
       <v-btn class="my-4" block> Undo
       </v-btn>
       <v-btn class="my-4" block> Redo
       </v-btn>
       <v-btn class="my-4" block> Erase
       </v-btn>
       <v-btn class="my-4" block> Draw
       </v-btn>
       <v-btn class="my-4" block> Clear
       </v-btn>
     </v-layout>
     <v-spacer></v-spacer>
     <!-- Canvas -->
     <!-- <v-card>
     </v-card> -->
      <v-card class="elevation-12" :width="card_width" :height="card_height">
            <canvas id="canvas"
              ref="canvas"
            ></canvas>
          </v-card>
     <v-layout column align-center justify-space-between fill-height>
       <v-row>
          <v-col
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
          </v-col>
          <!-- <v-col
            class="d-flex justify-center"
          >

          </v-col> -->
          <v-col
            class="d-flex justify-center"
          >
            <v-color-picker v-model="color"></v-color-picker>
          </v-col>
          <v-col
            cols="12"
            md="4"
          >
            <v-sheet
              dark
              class="pa-4"
            >
              <pre>{{ showColor }}</pre>
            </v-sheet>
          </v-col>
        </v-row>
      </v-layout>
    </v-layout>
  </v-container>
</template>

<script>
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
      mouseDown: false,
      mouseX: 0,
      mouseY: 0
    }),
    methods: {
      // after page loads, these even listeners come into play
      mounted(){
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

        this.$refs.addEventListener("mousedown", (e)=>{
            
            window.console.log("hello");
            this.mouseDown = true;
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;
            // print(this.mouseY);
            window.console.log(this.mouseX);
            window.console.log(this.mouseY);
        })
        this.$refs.canvas.addEventListener("mousedown", (e)=>{
            
            window.console.log("hello");
            this.mouseDown = true;
            this.mouseX = e.offsetX;
            this.mouseY = e.offsetY;
            // print(this.mouseY);
            window.console.log(this.mouseX);
            window.console.log(this.mouseY);
        })
        this.$refs.canvas.addEventListener("mouseup", ()=>{
        });
        // this.$refs.canvas.addEventListener("pointerdown", this.pointerdown);
        // this.$refs.canvas.addEventListener("pointermove", this.pointermove);
        // document.addEventListener("pointerup", this.pointerup);

      }

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
