# Philadelphia Museum of Art 

This study is a general attempt at finding data to build a small thing on top of. I took the lazy way out and came across the Philadelphia Museum of Art's ["hackathon"](https://hackathon.philamuseum.org/) page, which has been set up as a public-facing, experimental API. I appreciated the upfront-ness about this page, where it explicitly states that this is an experiment and that they are still in the early stages of infrastructure-building. "We're sharing our work-in-progress version of what could possibly become our collection data access layer with you." This is nice. 

So to celebrate how nice this open access to data was, with a quick and easy-to-use API, and how much I appreciate the Philadelphia Museum of Art for making this stuff available to me, a developer, I made a game about smashing up all the art in the museum. 

The premise of the game is simple (some could say... contrived). You are an Eagle avatar and the goal of the game is to smash up all the art in the museum because you are *extremely* excited about the Superbowl.

![](assets/images/pma1.jpg)

This game just continues forever, but you can get the screen to fill up with celebratory shouts.  

![](assets/images/pma3.jpg)

## Thoughts 

Understand that I am not trying to bring up problems, and my comments are not meant to be me complaining about something that was not intended to exist in the first place. Again, this API is noted to be experimental. 

- Documentation. I like that the out-of-the-box API framework provides all of the endpoints with which one could reach their data. I like that I can retrieve images of different kinds. What was lacking was information about the scope of the collections and what is appearing here (from smashing, they all seem to be from the same collection, and they are similar in style).

- Explorer. The API framework comes with an explorer tool so I can test out API calls right in my browser without having to set things up and deal with raw JSON data, reducing clumsiness and letting me get what I want more quickly, which is an understanding of what kind of data I can see and how I can grab it. 
