<template>

<form id="post-form" @submit.prevent="post()">

        <div class="container">
            <p v-if="errors.length">
                <b>Please correct the following error(s):</b>
            <ul>
                <li v-for="error in errors">{{ error }}</li>
            </ul>
            </p>
            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
            <input name="reply_to" id="reply_to" v-model="reply_to">
            <input name="icon" v-model="icon">
            <input name="name" v-model="name">
            <textarea name="body" id="body" v-model="body"></textarea>
            <button v-on:click="post()">Submit</button>
        </div>
</form>
</template>

<script>
    import axios from 'axios'
    export default {
        name: 'postform',
        /*
          Defines the data used by the component
        */
        data() {
            return {
                errors: [],
                name: '',
                icon: '',
                reply_to: '',
                body: '',
                file: ''
            }
        },

        methods: {
            /*
              Submits the file to the server
            */
            post() {
                /*
                        Initialize the form data
                    */
                var form = document.getElementById('post-form');

                let formData = new FormData(form);

                /*
                    Add the form data we need to submit
                */
                if(this.file) {
                    formData.append('file', this.file);
                }

                /*
                  Make the request to the POST /single-file URL
                */
                const options = {
                  method: 'POST',
                  headers: { 'content-type': 'application/x-www-form-urlencoded' },
                  data: formData,
                  url: '/post'
                };
                axios(options).then(function () {
                    console.log('SUCCESS!!');
                })
                    .catch((error) => {
                        this.errors = Object.values(error.response.data.error);
                    });
                return false;
            },

            /*
              Handles a change on the file upload
            */
            handleFileUpload() {
                this.file = this.$refs.file.files[0];
            }
        }
    }
</script>