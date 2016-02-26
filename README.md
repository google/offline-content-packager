Nkata
================

## What is it?
**This is not an official Google product.**
- Nkata is the Nigerian Igbo word for "basket". This is a content packaging tool, a configurable script that takes inputed media such as text and video, creates HTML shell pages around them, and bundles them into a navigable web-like experience with an index for use in an education setting without an Internet connection. Output (.zips, ISOs) can be burned onto external storage for loading onto unconnected machines. Examples of this content include:

    - Classroom Videos
    - Documentation (.PDFs, text files)
    - Tutorials
    - SDKs
    - Code Labs
    - eBooks (e.g. from O’Reily Open Books). etc.

- A homepage is generated for all the content that is bundled, with links to documentation pages, videos, and subsections. The homepage generation is controlled by configuration files.

- Transformations are run on the html files that are to be bundled. Any links to external (online) content are changed to a custom color (default is green); a bar is added to the top of each paging stating it is an offline version of that page; and an optional Google analytics tracking code is added.

- At the end, you can zip or create an ISO of your bundled offline content. The content can then be distributed via usb drive or DVD to those who do not have easy access to the internet.

## The Latest Version


- Details of the latest version can be found on https://github.com/google/offline-content-packager


## Prerequisites

- Nkata needs a version of Python 2.7.x and above installed

Note: For windows a version of Python 3.2.x and above should be installed.


## Installation


- To install Nkata: offline-content-packager:
    - `clone nkata (git clone https://github.com/google/offline-content-packager.git)`
    - `cd into nkata`
    then
    - `pip install -r requirements.txt`
    - `pip install --editable .`


## Main Configuration File

- The main configuration file is used to define the source directory, destination directory, and organization of the content to be bundled. The information in the main config file, and section config files, is used to create a homepage for your bundled content.

- Inside the root directory of this tool we should have our configuration file, config.yaml. For example:

    ```
    ---
      project_title: "Google Offline Content Packaging Tool"  // The name given to the content to be bundled
      project_subtitle: "Google Offline Package Test..."   // Extra information about the overall content
      absolute_link_color: "green"  // The color used to style all absolute links on the page, green by defaults
      tracking_code: "XX-XXXXXXXX-X" // Google analytics tracking ID
      output_folder_name: "goc"
      source:
        main_path: "build/source" // The top directory for the content(s) to be processed
        video_source: "videos"
      destination:
        main_path: "build/output" // Where you like the processed content(s) to be saved.
      version: "1.0.0"
      division: // Where you specify where each section should be placed when splitting content(s)
        disc1:
         - sample_section 1
         - sample_section 2
        disc2:
         - sample_section 3
         - sample_section 4
    ```

## Configuration for each Section

- Inside the sample source directory of this tool, there are sections. Each section has a configuration file, namely section_config.yaml. For example:

    ```
    ---
      title: "Introduction to Android"  // The title given to the content in the section
      online_link: "http://developer.android.com/intl/ko/guide/index.html" // Link to online version
      metadata:
      -
        title: "Fixing Bugs"    // The name for linked content, used on the generated homepage
        filename: "index.html"  // The file to link to
      -
        title: "Basic Android Concepts"
        filename: "main.html"
    ```

## Configuration for Videos

- Inside the sample source directory of this tool there is a videos directory. In the videos directory, we  divide the videos into various sections, each of which can have its own configuration file, named section_config.yaml. For example, in a section called Android:

    ```
    ---
      video_subtitle: "This section contains some introductory videos on Introduction to Android"
      video_summary: "Introduction to Android Videos"
      template_path: ""
      metadata: // Paths to metadata.
        sample1: "build/source_files/videos/Android/metadata/sample1_metadata.yaml"
        sample2: "build/source_files/videos/Android/metadata/sample2_metadata.yaml"
        sample3: "build/source_files/videos/Android/metadata/sample3_metadata.yaml"
    ```
- By default, the title of a video will be the same as its filename. If you’d like to change this, or specify additional information such as a description, you can do so with a config file in the metadata directory. For example:

    ```
    ---
      title: "Basic Android Concepts"
      description: "Introductory Android Concepts Videos"
      sub_title: "Introductory Android Videos"
      thumbnail_url: "<thumbnail_url link>"
    ```

  NOTE :
  - You can edit any of the above configuration files to suit your purpose.
  - You can generate metadata for a video by running:
    ```
    nkata generate -t metadata -u <URL>
    ```
  - You can also generate metadata for each section in the video directory by adding videos_url.yaml for each section. For example:

    ```
    ---
      urls:
      -
        video_name: "01 - Accessibility and Localization - Intro"
        url: "<URL>"
      -
        video_name: "02 - Reaching All Users"
        url: "<URL>"
    ```
    then run:
    ```
    nkata generate -t auto
    ```


## Documentation


- Run `nkata` to see list of commands

  Basic usage:
    - `nkata bundle`

  only bundle videos:
    - `nkata bundle_videos`

  convert to zip and ISO:
    - `nkata convert`


## Licensing

- Copyright 2015 The Offline Content Packager Authors. All rights reserved.


  - Licensed to the Apache Software Foundation (ASF) under one or more contributor
license agreements.  See the NOTICE file distributed with this work for
additional information regarding copyright ownership.  The ASF licenses this
file to you under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License.  You may obtain a copy of
the License at http://www.apache.org/licenses/LICENSE-2.0

  - Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
License for the specific language governing permissions and limitations under
the License.

##Mailing List

The project mailing list is offline-content-packager@googlegroups.com. The list will be used for announcements, discussions, and general support. You can subscribe via [groups.google.com](https://groups.google.com/forum/#!forum/offline-content-packager).


## Changelog

- 1.0.0
  - initial release
