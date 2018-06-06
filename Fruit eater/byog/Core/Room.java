package byog.Core;

import byog.Core.Nodes.TileNode;

public class Room {

    /*
        This is the Room class. This class is responsible for
        storing its own construction information,
        housing the TileNode subclass,
        and providing its construction information.

        IT IS NOT RESPONSIBLE FOR CONSTRUCTING ITSELF!
        IT MERELY PROVIDES THE INFORMATION TO CONSTRUCT ITSELF!


        (\  _ _/)                                       (\     /)
        (  ='.'=) Omae wa mou Shin deiru...     Nani!?  (=O_O=  )
       /(")<DB>(")                                      (")<BB>(")
        And Debugger Bunny struck down Bugs Bunny.
     */

    private int width; //width of the room.
    private int height; //height of the room.
    private TileNode origin; //The starting x y position stored in the
    private TileNode hallnode;
    private TileNode[] corners;
    private Room[] neighbors;
    private Room[] attachments;
    private int neighborcount;
    private int attachmentcount;

    public Room(int[] specs) {
        /*
            specs structure is generally: {width, height, x_cor, y_cor, x_node, y_node}
            x_node and y_node refer to the hallway nodes that will serve as terminals for
            the hallways.
         */
        width = specs[0];
        height = specs[1];
        origin = new TileNode(specs[2], specs[3]);
        hallnode = new TileNode(specs[4], specs[5]);
        corners = new TileNode[] {
            origin,
            new TileNode(specs[2], specs[3] + height),
            new TileNode(specs[2] + width, specs[3]),
            new TileNode(specs[2] + width, specs[3] + height)
        };
        neighbors = new Room[3];
        attachments = new Room[2];
        neighborcount = 0;
        attachmentcount = 0;
    }

    public boolean contains(Room room) {
        boolean in = false;
        for (Room n : attachments) {
            if (room == n) {
                in = true;
                break;
            }
        }
        return in;
    }

    public void addneighbor(Room neighbor) {
        if (neighborcount < neighbors.length) {
            neighbors[neighborcount] = neighbor;
            neighborcount++;
        }
    }

    public int[] dimensions() {
        //Provides an int array with the dimensions of the room
        return new int[] {width, height};
    }

    public void addAttachment(Room room) {
        if (attachmentcount < attachments.length) {
            attachments[attachmentcount] = room;
            attachmentcount += 1;
        }
    }

    public Room[] getneighbors() {
        return neighbors;
    }

    public int[] getHallnode() {
        return hallnode.getcoords();
    }

    public TileNode getNode() {
        return hallnode;
    }

    public int[][] roomBP() {
        //Provides a 2D array with room schematics.
        int[][] blueprint = new int[3][];
        blueprint[0] = dimensions(); //Room dimensions.
        blueprint[1] = origin.getcoords(); //Room starting xy coords.
        blueprint[2] = hallnode.getcoords(); //Hallway node coordinates.
        return blueprint;
    }

    public TileNode getcorner(int i) {
        /*
            Conveniently access a specific corner.
            0 = bottom left
            1 = top left
            2 = bottom right
            3 = top right
        */

        if (i >= corners.length) {
            return null;
        } else {
            return corners[i];
        }
    }

}
