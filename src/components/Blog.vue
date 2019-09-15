<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="title" placeholder="请输入标题" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="body"></el-input>
        <el-button type="primary" @click="addBlog()" style="float:left; margin: 2px;">新增</el-button>
        <el-button type="primary" @click="postBlog()" style="float:left; margin: 2px;">new</el-button>
    </el-row>
    <el-row>
        <el-table :data="blogs" style="width: 100%" border>
          <el-table-column prop="url" label="编号" min-width="100">
            <template scope="scope"> {{ scope.row.url }} </template>
          </el-table-column>
          <el-table-column prop="title" label="标题" min-width="100">
            <template scope="scope" contenteditable="true"> {{ scope.row.title }} </template>
          </el-table-column>
          <el-table-column prop="body" label="内容" min-width="100">
            <template scope="scope"> {{ scope.row.body }} </template>
          </el-table-column>
          <el-table-column prop="created" label="添加时间" min-width="100">
            <template scope="scope"> {{ formatDate(scope.row.created) }} </template>
          </el-table-column>
          <el-table-column>
            <template slot-scope="scope">
                <el-button size="small" type="danger" @click="delBlog(scope.row.url)">删除</el-button>
                <el-button size="small" type="primary" @click="updateBlog(scope.row)">更新</el-button>
            </template>
          </el-table-column>
        </el-table>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'
import axios from 'axios'


export default {
  name: 'blog',
  data () {
    return {
      title: 'go',
      body: 'blog',
      url: 'http://127.0.0.1:8000/app/blogs/',
      blogs: [],
    }
  },
  mounted: function() {
      this.showBlogs()
  },
  methods: {
    addBlog() {
        var data = {title: this.title, body: this.body}
        fetch(this.url, {
            method: 'POST', // or 'PUT'
            body: JSON.stringify(data),
            headers:{'Content-Type': 'application/json'}
            }).then(res => res.json())
            .then(response => {
                console.log('Success:', JSON.stringify(response))
                this.blogs.push(response)
            })
            .catch(error => console.error('Error:', error));
    },
    postBlog() {
        var data = {title: this.title, body: this.body}
        axios.post(this.url, data)
        .then(response => {
          this.blogs.unshift(response.data);
          console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    delBlog (url) {
        axios.delete(url)
        .then(resp => {
            console.log(resp)
            this.blogs = this.blogs.filter(result => {
                return result.url != url;
            })
        }).catch(function (error) {
            console.log(error);
        });
    },
    showBlogs(){
        fetch(this.url)
        .then(resp => resp.json())
        .then(data => {
            this.blogs = data
        })
    },
    formatDate (value, fmt = 'YYYY-MM-DD') {
      return (value == null)
        ? ''
        : moment(value, 'YYYY-MM-DD').format(fmt)
    },
    updateBlog (blog) {

        console.log(blog.title, blog.body)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
