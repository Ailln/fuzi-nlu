<template>
  <div id="app">
    <div id="github">
      <Button
        @click="buttonClick"
        size="large"
        shape="circle"
        icon="logo-github"
        >More in Github</Button
      >
    </div>
    <div id="chatbot">
      <Card :bordered="false" id="content">
        <p slot="title">🤖️ ChatBot</p>
        <!-- eslint-disable -->
        <div v-if="this.messageList.length > 9">
          <Scroll height="410">
            <div v-for="messageItem in messageList">
              <div v-if="messageItem.user">
                <Button id="question" type="primary" ghost>{{
                  messageItem.msg
                }}</Button>
              </div>
              <div v-else>
                <Button id="answer" type="primary" ghost>{{
                  messageItem.msg
                }}</Button>
              </div>
              <br />
              <br />
            </div>
          </Scroll>
        </div>
        <div v-else>
          <div v-for="messageItem in messageList">
            <div v-if="messageItem.user">
              <Button id="question" type="primary" ghost>{{
                messageItem.msg
              }}</Button>
            </div>
            <div v-else>
              <Button id="answer" type="primary" ghost>{{
                messageItem.msg
              }}</Button>
            </div>
            <br />
            <br />
          </div>
        </div>
      </Card>
      <div id="send">
        <Input
          v-model="questionMessage"
          search
          enter-button="发送"
          size="large"
          placeholder="Enter something..."
          @on-search="sendQuestionMessage"
        />
      </div>
      <div style="text-align: center; width: 800px; margin: 20px auto">
        <Alert type="info" show-icon style="line-height: 2">
          注：该 DEMO 仅包含我随意编写的几十条训练样本，主要是关于我家猫「锅贴」的介绍，这些只发挥了该项目的一小部分功能。<br>
          当然你也自定义数据来丰富聊天机器人的功能，这里提供了构建数据集的 <Button style="padding: 0; margin: 0; color: #2d8cf0;"  to="./labeling" target="_blank" type="text" size="small">可视化工具 Labeling</Button>。
        </Alert>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  sockets: {
    connect: function() {
      // eslint-disable-next-line
      console.log('socket: connected')
    },
    response: function(data) {
      this.messageList.push({ user: 0, msg: data.msg })
      // eslint-disable-next-line
      console.log('receive: ', data)
    },
  },
  data() {
    return {
      questionMessage: '',
      messageList: [
        {
          user: 0,
          msg:
            '新功能：支持「中文数字」和「阿拉伯数字」转化，需要在转化句子前加入「cn2an:」或者「an2cn:」。',
        },
        { user: 1, msg: '你好！' },
        {
          user: 0,
          msg: '你好啊～我是由 Ailln 开发的智能机器人——「锅贴」。',
        },
        {
          user: 0,
          msg: '现在试试对我说：你叫什么名字吧？',
        },
      ],
    }
  },
  methods: {
    sendQuestionMessage() {
      if (this.questionMessage === '') {
        this.$Notice.warning({
          title: '请输入内容！',
        })
      } else {
        this.messageList.push({ user: 1, msg: this.questionMessage })
        this.$socket.emit('receive', this.questionMessage)
        this.questionMessage = ''
      }
    },
    buttonClick() {
      window.open('https://github.com/Ailln/chatbot', 'target', '')
    },
  },
}
</script>

<style>
#github {
  width: 146px;
  margin: 40px auto;
}

#chatbot {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 40px auto;
  width: 800px;
}

#content {
  border-radius: 10px;
  height: 500px;
}

#send {
  margin: 30px 150px;
}

#question {
  float: right;
  margin: 10px 10px 10px 100px;
  text-align: left;
}

#answer {
  float: left;
  margin: 10px 100px 10px 10px;
  text-align: left;
}
</style>
