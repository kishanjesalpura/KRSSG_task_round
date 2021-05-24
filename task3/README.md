# The RRT* conneect algorithm

---

## Files intro (:D)
 - The file RRT star connect has the rrt star connect programme that implements rrt* connect in map1 (i can say perfectly) I have also commented out some part of the program to not print the maps of the nodes bcus it was making the image look very messy.
 - Now just copy the folder in and run the rrtstar connect algo u will straightawa get the image of the best path that it can find to the goal and also by taking out hte lst two commented lines u will get the individual maps of the start and goal trees.
 - and the middle big commented path will show u trees connections and also the best path.
 
 ---
 
 - In the rrt* for map 2 file I was not able to get all the 3 different circles centres using houghcircles method in opencv not sure of hte error but if i get that i am almost done with it.
 
 ---

 - in the try rrt star file i tried to make the interpolation using all the node points but was not able to succeed.
 - the reason that i suspect is that to find the interpolation i need a function (i.e for any one value of x there should be only one value of y like in standrd definition of circle in math.) for that type of curves interpolation is a bit easy but my curve formed is not a function hence it can not form the interpolation(thought this is a wild guess from my side).