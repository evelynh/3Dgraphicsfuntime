<template>
<div  width="60%">
3D PREVIEW: 
<model-obj 
        :backgroundColor="bgColor"
        src="windmill.obj"
        margin= "10px"
        >
    </model-obj>
    </div>
</template>
<script>

import { ModelObj } from 'vue-3d-model';
export default {
  components: { ModelObj },
  data () {
    return {
        bgColor: "#ADD8E6",
    }
    }
}
</script>

