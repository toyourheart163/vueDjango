<template>
  <div class="home">
    <vxe-toolbar>
      <template v-slot:buttons>
        <vxe-button @click="$refs.xTable.toggleRowSelection(blogs[1])">切换第二行选中</vxe-button>
        <vxe-button @click="$refs.xTable.setSelection([blogs[2], blogs[3]], true)">设置第三、四行选中</vxe-button>
        <vxe-button @click="$refs.xTable.setAllSelection(true)">设置所有行选中</vxe-button>
        <vxe-button @click="$refs.xTable.clearSelection()">清除所有行选中</vxe-button>
        <vxe-button @click="getSelectEvent">获取选中</vxe-button>            
        <vxe-button @click="exportCsvEvent">默认导出</vxe-button>
      </template>
    </vxe-toolbar>
    <vxe-table 
      border
      resizable
      show-overflow
      highlight-hover-row
      :data="blogs"
      :loading="loading"
      ref="xTable"
      @cell-click="cellClickEvent"
      @select-all="selectAllEvent"
      @select-change="selectChangeEvent"
      :edit-config="{trigger: 'dblclick', mode: 'row'}"
    >
      <!-- <vxe-table-column type="selection" width="60"></vxe-table-column> -->
      <vxe-table-column type="index" title="序号" width="80"></vxe-table-column>
      <vxe-table-column field="title" title="标题" sortable :edit-render="{name: 'input'}"></vxe-table-column>
      <vxe-table-column field="visited" title="访问" sortable :edit-render="{name: 'input'}"></vxe-table-column>
      <vxe-table-column field="body" title="内容" sortable :edit-render="{name: 'input'}"></vxe-table-column>
      <vxe-table-column field="created" title="时间" ></vxe-table-column>
      <vxe-table-column title="操作">
            <template v-slot="{ row }">
              <template v-if="$refs.xTable.hasActiveRow(row)">
                <vxe-button @click="saveRowEvent(row)">保存</vxe-button>
                <vxe-button @click="cancelRowEvent(row)">取消</vxe-button>
              </template>
              <template v-else>
                <vxe-button @click="delBlog(row.url)">del</vxe-button>
                <vxe-button @click="editRowEvent(row)">编辑</vxe-button>
              </template>
            </template>
          </vxe-table-column>
    </vxe-table>

    <input type="text" v-model="title">
    <input type="text" v-model="body">
    <vxe-button @click="addBlog">addblog</vxe-button>
    <vxe-grid
      border
      resizable
      height="300"
      :columns="tableColumns"
      :edit-config="{trigger: 'click', mode: 'row', showStatus: true}"
      :start-index="(tablePage.currentPage - 1) * tablePage.pageSize"
      :pager-config="tablePage"
      @page-change="handlePageChange"
      show-footer
      :footer-method="footerMethod"
      :data="blogs"></vxe-grid>
  </div>
</template>

<script>
import moment from 'moment'
import axios from 'axios'

export default {
  name: 'blog',
  data () {
    return {
      loading: false,
      title: 'go',
      body: 'blog',
      url: 'http://127.0.0.1:8000/app/blogs/',
      blogs: [],
      tableColumns: [
        {type: 'index', width: 50},
        {field: 'url', title: 'id', editRender: {name: 'input'}},
        {field: 'title', title: '标题', editRender: {name: 'input'}},
        {field: 'visited', title: '访问', editRender: {name: 'input'}},
        {field: 'body', title: '内容', showHeaderOverflow: true, editRender: {name: 'input'}},
        {field: 'created', title: '时间', showOverflow: true}
      ],
      tablePage: {
        total: 0,
        currentPage: 1,
        pageSize: 5
      }
    }
  },
  mounted: function () {
    this.showBlogs()
  },
  methods: {
    addBlog () {
      var data = {title: this.title, body: this.body}
      fetch(this.url, {
        method: 'POST', // or 'PUT'
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
      }).then(res => res.json())
        .then(response => {
          console.log('Success:', JSON.stringify(response))
          this.blogs.push(response)
        })
        .catch(error => console.error('Error:', error))
    },
    postBlog () {
      var data = {title: this.title, body: this.body}
      axios.post(this.url, data)
      .then(response => {
        this.blogs.unshift(response.data)
        console.log(response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    delBlog (url) {
      axios.delete(url)
      .then(resp => {
        console.log(resp)
        this.blogs = this.blogs.filter(result => {
          return result.url !== url
        })
      }).catch(function (error) {
        console.log(error)
      })
    },
    showBlogs () {
      this.loading = true
      setTimeout(() => {
        const page = this.tablePage
        fetch(this.url + '?limit=' + page.pageSize + '&offset=' + page.pageSize * (page.currentPage - 1))
        .then(resp => resp.json())
        .then(data => {
          this.blogs = data.results
          this.tablePage.total = data.count
        })
        this.loading = false
      }, 300)
    },
    formatDate ({value, row, column}) {
      return (value == null)
        ? ''
        : moment(value, 'YYYY-MM-DD').format('YYYY-MM-DD')
    },
    updateBlog (blog) {
      console.log(blog.title, blog.body)
    },
    cellClickEvent () {
      console.log('单元格点击事件')
    },
    selectAllEvent ({ checked }) {
      console.log(checked ? '所有勾选事件' : '所有取消事件')
    },
    selectChangeEvent ({ checked, row }) {
      console.log(checked ? '勾选事件' : '取消事件')
    },
    getSelectEvent () {
      let updateRecords = this.$refs.xTable.getSelectRecords()
      this.$XModal.alert(updateRecords.length)
    },
    exportCsvEvent () {
      this.$refs.xTable.exportCsv()
    },
    handlePageChange ({currentPage, pageSize}) {
      this.tablePage.currentPage = currentPage
      this.tablePage.pageSize = pageSize
      this.showBlogs()
    },
    footerMethod ({ columns, data }) {
      return [
        columns.map((column, columnIndex) => {
          if (columnIndex === 0) {
            return '平均'
          }
          if (['visited'].includes(column.property)) {
            return this.$utils.mean(data, column.property)
          }
          return null
        }),
        columns.map((column, columnIndex) => {
          if (columnIndex === 0) {
            return '和值'
          }
          if (['visited'].includes(column.property)) {
            return this.$utils.sum(data, column.property)
          }
          return null
        })
      ]
    },
    editRowEvent (row) {
      this.$refs.xTable.setActiveRow(row)
    },
    saveRowEvent (row) {
      var data = {title: row.title, body: row.body, visited: row.visited}
      axios.put(row.url, data)
      .then(response => {
        console.log(response.data)
        this.cancelRowEvent()
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancelRowEvent (row) {
      this.$refs.xTable.clearActived()
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
