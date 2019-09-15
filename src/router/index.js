import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Blog from '@/components/Blog'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/',
      name: 'blog',
      component: Blog
    },
    
  ]
})
