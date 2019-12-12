<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Digital Humanities Project</span>
        <span class="font-weight-light">3D Graphics Fun Time</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        text
        href="https://github.com/evelynh/3Dgraphicsfuntime"
        target="_blank"
      >
        <span class="mr-2">Project GitHub</span>
      </v-btn>
      <v-btn text class="mr-2" @click.stop="dialog = true"> ABOUT </v-btn>
      <v-dialog
      v-model="dialog"
      max-width="800"
      >
      <v-card>
        <v-card-title class="font-weight-black">ABOUT TEDDY</v-card-title>
        <v-card-text>
          <!-- <div class="headline font-italic" font-weight="500em" font-size="100px"> WHO DEVELOPED TEDDY </div> -->
          <v-btn block disabled=true>WHO DEVELOPED TEDDY</v-btn>
          Teddy was developed in 1999 by Takeo Igarashi, Satoshi Matsuoka and Hidehiko Tanaka from the 
          University of Tokyo and Tokyo Institute of Technology. The Teddy paper was published in the
          1999 ACM SIGGRAPH Conference.
          <v-btn block disabled=true>WHAT IS TEDDY</v-btn>
           <!-- <div class="headline font-italic" font-weight="500em"> WHAT IS TEDDY </div> -->
          Teddy is a 2D to 3D sketching interface, used to efficiently design freeform models
          such as stuffed animals (hence the name!) and rotund objects. There are also several later
          iterations of the Teddy System such as Chameleon which allows for textures, and SmoothTeddy, 
          which includes a painting software.
          <v-btn block disabled=true>3D FUNTIME & TEDDY</v-btn>
          <!-- <div class="headline font-italic" font-weight="500em"> 3D FUNTIME & TEDDY </div> -->
          For our project, we wanted to emulate the first Teddy System, where a user can draw any object
          on a 2D canvas, and the object is then rendered into a 3D polygonal surface. 
          On the main page, draw whatever shape you desire, the press submit to see your drawing rendered in 3D!
           </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            DONE
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </v-app-bar>
    <v-content>
      <div id="app">
        <router-view/>
      </div>
    </v-content>
  </v-app>
</template>

<script>
  // export default {
  //   name: 'App',
  //   data:() => ({
  //     dialog: false,
  //   })
  // }
// <template>
//   <v-app>
//     <v-app-bar
//       app
//       color="primary"
//       dark
//     >
//       <div class="d-flex align-center">
//         <v-img
//           alt="Vuetify Logo"
//           class="shrink mr-2"
//           contain
//           src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
//           transition="scale-transition"
//           width="40"
//         />

//         <v-img
//           alt="Vuetify Name"
//           class="shrink mt-1 hidden-sm-and-down"
//           contain
//           min-width="100"
//           src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
//           width="100"
//         />
//       </div>

//       <v-spacer></v-spacer>

//       <v-btn
//         href="https://github.com/vuetifyjs/vuetify/releases/latest"
//         target="_blank"
//         text
//       >
//         <span class="mr-2">Latest Release</span>
//         <v-icon>mdi-open-in-new</v-icon>
//       </v-btn>
//     </v-app-bar>

//     <v-content>
//       <HelloWorld/>
//     </v-content>
//   </v-app>
// </template>

// import HelloWorld from '../components/HelloWorld';

export default {
  name: 'App',

  // components: {
  //   HelloWorld,
  // },

  data: () => ({
    dialog: false,

  }),
};
</script>
