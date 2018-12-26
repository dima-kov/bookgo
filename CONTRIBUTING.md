# Deployment

1. `git clone https://github.com/dima-kov/bookgo.git`
2. `cd bookgo`
3. `mkdir src`
4. `mv -v * ./src`
5. `cd src`
6. `make install_local`

# Front

1. Install Node.JS
2. Install dependencies: `npm install`

## Usage
1. `gulp less` - generate css from less
2. `gulp minify-css` - minify css
3. See more in `gulpfile.js`


## Sub domains system usage

1. Sites
    Edit default Site object (with id=1 !Important), set
        slug=`bookgo.com`  
        display_name=```

1. Club. Create some clubs. E.g.:
    Club(slug='pekar')
    
1. Edit /etc/hosts for local development:
    
    127.0.0.1 pekar.bookgo.com
    127.0.0.1 bookgo.com

1. Access via:
    
    ```
    pekar.bookgo.com:8000
    
    bookgo.com:8000
    
    127.0.0.1:8000
    ```
