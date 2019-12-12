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
    </v-app-bar>
    <v-content>
      <div id="app">
        <router-view/>
      </div>
    </v-content>
  </v-app>
</template>

<script>
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
    //
  }),
};
</script>
