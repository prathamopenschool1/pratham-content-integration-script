PraDigi Sushi Chef
==================
Scripts to import content from prathamopenschool.org website into Kolibri Studio.



Install
-------

### 1. get the code

    git clone https://github.com/prathamopenschool1/pratham-content-integration-script.git
    cd pradigisushichef/

### 2. setup a python virtual environment

    virtualenv -p python3 prathamenv
    source prathamenv/bin/activate
    pip install -r requirements.txt



Running
-------
To run the chef script, follow these steps:

### 1. Go the the project directory


    cd pradigisushichef

### 2. Activate the virtual env

    source venv/bin/activate


### 3. Clear the web caches

    rm -rf .webcache
    rm -rf cache.sqlite


### 4. Run the chef script:

    python pradigichef.py --token=<your_token>


This commands takes 19+ hours the first time it runs and performs the following:

  - During the `pre_run` stage:
    - crawl all languages https://www.prathamopenschool.org website
      output: json data in `chefdata/trees/pradigi_{lang}_web_resource_tree.json`
    - Builds the channel ricecooker tree:
      output: json data in `chefdata/trees/pradigi_ricecooker_json_tree.json`
    - Build HTML5Zip files from PraDigi games and webapps (saved in `chefdata/zipfiles`)

  - During the `run` stage, it tuns the `uploadchannel` command (multiple steps:
    - Load tree spec from `chefdata/trees/pradigi_ricecooker_json_tree.json`
    - Build ricecooker class tree (Python classes) from json spec
    - Download all files to `storage/` (remembering paths downloaded to `.ricecookerfilecache/`)
    - Run compression steps for videos and store compressed output in `storage/` (also `.ricecookerfilecache/`)
    - Run validation logic (check required metadata and all files present)
    - Upload content to Kolibri Studio

On subsequent runs, the process will use cached version of files downloaded,
generated HTML5Zip files, and compressed videos to avoid the need to re-download
everything.

When source files change or are modified, you can run a "clean start" chef run
but doing the following steps:
  - clear zip file cache `rm -rf chefdata/zipfiles`
  - clear web caches `rm -rf .webcache` and `rm -rf cache.sqlite`
  - clear storage dir `rm -rf storage/`
Note this will take 15+ hours again since we have to redo all the download and
conversion steps.

IMPORTANT: We recommend that you run `rm -rf .webcache` and `rm -rf cache.sqlite`
manually every time the website changes.



LE variant of the channel
-------------------------
There are two variants of the PraDigi channel, the `LE` variant is the "official"
version that is PUBLIC channel on Studio that all Kolibri users can see and import.
The `PRATHAM` variant is almost identical, but includes extra "debug info" in the
descriptions of each content node. The PRATHAM variant is maintained by Pratham.

To run the Learning Equality (LE) variant use the following command:

    python pradigichef.py --token=<your_token>  variant=LE

Note the extra command line option `varian=LE` passed in to select the LE variant.


### Running on vader

To run the chef in the background using (useful when running on a remote server via ssh):

    ssh chef@vader
        cd pradigisushichef
            rm -rf .webcache
            source venv/bin/activate
            nohup python pradigichef.py --token=<your_token> --stage variant=LE &

The output of the script will be saved to the local file `nohup.out`, which you
can "follow" by using `tail -f nohup.out` to monitor the chef run.
