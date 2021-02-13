# Eufy Doorbell Reset Doorbell Chime
This code lets you reset your doorbell chime if it begins to hang/buzz between the "ding" and "dong" of a chime.

## Problem
My Eufy Wireless Video Doorbell (which is wired -- for the purpose of allowing me to use my own mechanical chime, don't ask me why they made it this way) after 2-3 days of idling, it will send a longer pulse over time to my mechanical doorbell. This results in an immediate "ding", but a longer pause and buzzing before the "dong". This can be seen in the video here: https://imgur.com/a/db6HG3L

## Solution
Oddly enough, switching between the mechanical and digital chime and back to the mechanical chime fixes the problem for a few days. To simulate this on a server nightly as a cron job, a Python script would take care of this.

To perform this, I determined the P2P commands to send by capturing the pcap on the mobile device and then replayed those commands.

## Setup

None of this could have been done without Jan Loebel's framework and Wireshark Lua script: https://github.com/JanLoebel/eufy-node-client-examples. While his framework aims to achieve the similar goal of sending P2P commands, for my specific needs, it did not work and needed to be slightly altered.

1. With the link above, follow the directions for "Getting started" and write down the P2P_DID and the ACTOR_ID (account ID).
2. Determine the IP of your Homebase2 base station (this can be found in the app settings)
3. Determine the IP of where the script will be running
4. Replace all of the empty variables in the beginning of the script with these items
5. Make sure that your doorbell chime is currently set to an on state

I can't guarantee that this will work for everyone, and this code is far from perfect and probably has a lot of bugs. But hopefully this can at least get you on the right path for fixing your doorbell ringing issues.
