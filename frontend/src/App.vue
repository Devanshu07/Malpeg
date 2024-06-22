<template>
  <div id="app" v-bind:class="{'red' : isMalicious, 'green' : isBenign , 'white' : yetToCheck}">
    <h1 v-bind:class="{'white-text': !yetToCheck}">MALJPEG</h1>
    <br><br>
    <picture-input
      ref="pictureInput"
      @change="onChange"
      @removed="onRemoved"
      width="300"
      height="300"
      margin="16"
      accept="image/jpeg,image/jpg"
      size="10"
      :removable="true"
      :customStrings = "{
        upload: '<h1>Bummer!</h1>',
        drag: 'Drag a JPEG image'
      }">
    </picture-input>

    <button @click="attemptUpload" v-bind:class="{disabled: !this.image}">
      Upload
    </button>

    <h2 class="result" v-if="isBenign">BENIGN</h2>
    <h2 class="result" v-if="isMalicious">MALICIOUS</h2>
  
  </div>
</template>

<script>
import axios from 'axios'
import PictureInput from 'vue-picture-input'

export default {
  name: 'App',
  components: {
    PictureInput
  },
  data() {
    return {
    'checkimage': null,
    'imageClass': "",
    isBenign: false,
    isMalicious: false,
    yetToCheck: true,

    };
  },
  methods: {
    onChange () {
      console.log('New picture selected')
      if (this.$refs.pictureInput.image) {
        console.log('Picture loaded.')
        //console.log(this.$refs.pictureInput.image.slice(23))
        this.checkimage = this.$refs.pictureInput.image.slice(23) 
        this.yetToCheck = true
        this.isBenign = false
        this.isMalicious = false
      } else {
        console.log('FileReader API not supported')
      }
    },
    onRemoved () {
      this.yetToCheck = true
      this.isBenign = false
      this.isMalicious = false,
      this.image = ""
    } ,
    attemptUpload() {
      const path = 'http://localhost:5000/predict'
      axios.post(path, {"image": this.checkimage}).then(response=>{
        this.imageClass = response.data["class"]
        if (this.imageClass == "malicious") {
          this.isMalicious = true
          this.isBenign = false
          this.yetToCheck = false
          var audio1 = new Audio(require('./virus.mp3'))
          audio1.play()
        } else {
          var audio2 = new Audio(require('./safe.mp3'))
          audio2.play()
          this.isBenign = true
          this.isMalicious = false
          this.yetToCheck = false
        }
      })
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: absolute;
  top: 0px;
  right: 0px;
  left: 0px;
  bottom: 0px;
}

.red {
  background: red;
}

.green {
  background: green;
}

.white {
  background: honeydew;
}

.white-text {
  color: white;
}

.result {
  color: white;
}
</style>
