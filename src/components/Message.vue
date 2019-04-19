<template>
    <div v-bind:class="'message '+(state.replying?'replying':'')">
        <div v-show="state.replying">Replying...<button @click="reply(null)">Cancel</button></div>
        <div style="margin-left:100px">
            <message v-for="message in reply_to" v-bind:message="message" v-bind:key="message.count"
                     v-if="root"></message>
        </div>
        {{ message.datetime|formatDate }} {{ message.count }} {{ message.ident }}
        <div class="header">
            <span v-if="!message.icon && message.location">
                <img v-bind:src="'/static/icons/countries/'+message.location.country+'.png'">
                <img v-if="message.location.region" v-bind:src="'/static/icons/countries/'+message.location.country+'-'+message.location.region+'.png'">
            </span>
            <span v-if="message.icon">
                <img v-bind:src="'/static/icons/tripflags/'+message.icon+'.png'">
            </span>
            {{ message.name }}

        </div>
        <div v-if="message.file">
            <img v-if="message.file.type == 'image'" :class="state.expanded?'expanded':'picture'" v-bind:src="'/static/uploads/'+(state.expanded?message.file.file:message.file.thumb)" @click="expand">
            <a :href="'/static/uploads/'+message.file.file" target="_blank" v-if="message.file.type == 'video'"><img v-bind:src="'/static/uploads/'+(state.expanded?message.file.file:message.file.thumb)"></a>
            <div class="filename">
                <a :href="'/static/uploads/'+message.file.file" target="_blank">{{ message.file.filename }}</a>
                <span v-if="message.file.width">{{message.file.width}}x{{message.file.height}}</span>
                {{ message.file.size | fileSize}}
            </div>
        </div>
        <div class="body">{{ message.body }}</div>
        <button @click="reply(message)">reply</button>
        <button @click="ignore(message)">ignore</button>
    </div>
</template>

<script>

    export default {
        name: 'message',
        props: ['message', 'root'],
        computed: {
            reply_to: function () {
                if (!this.message.reply_to) return []
                return this.message.reply_to.map(function (count) {
                    return chat.messages_by_count[count]
                }).filter(message => message)
            }
        },
        data: function () {
            return {
                state:{replying: false, expanded: false}
            }
        },
        methods: {
            reply: function (message) {
                this.$root.$emit('replying');
                if(message) {
                    this.state.replying = true;
                    document.getElementById('reply_to').value = message.count;
                } else {
                    document.getElementById('reply_to').value = '';
                }
            },
            ignore: function (message) {

            },
            expand: function() {
                this.state.expanded = !this.state.expanded;
            }
        },
        mounted: function () {
            this.$root.$on('replying', () => {
                this.state.replying = false;
            })
        }
    }
</script>