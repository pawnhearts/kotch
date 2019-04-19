<template>
    <div v-bind:class="'message '+(state.replying?'replying':'')">
        <div v-show="state.replying">Replying...<button @click="reply(null)">Cancel</button></div>
        <div style="margin-left:100px">
            <message v-for="message in reply_to" v-bind:message="message" v-bind:key="message.count"
                     v-if="root"></message>
        </div>
        {{ message.datetime|formatDate }} {{ message.count }} {{ message.ident }}
        <div class="header"><img v-bind:src="'/static/icons/countries/'+message.country.split('-')[0]+'.png'"><img
                v-if="message.country.indexOf('-') !== -1"
                v-bind:src="'/static/icons/countries/'+message.country+'.png'">{{ message.name }}
        </div>
        <div v-if="message.file">
            <img :class="state.expanded?'expanded':'picture'" v-bind:src="'/static/uploads/'+message.file" @click="expand">
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
                })
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