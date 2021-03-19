<template>
     <!-- 所有的内容要被根节点包含起来 -->
    <div id="home">    

      
    </div>
</template>


<script>
import { mapGetters } from 'vuex'


export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  methods: {
  },
  data() {
    return {
    }
  },
   mounted() {
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
