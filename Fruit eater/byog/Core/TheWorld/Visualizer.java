package byog.Core.TheWorld;

import java.util.Random;
import byog.Core.Room;
import byog.TileEngine.TETile;
import byog.TileEngine.Tileset;

public class Visualizer {

    private int width;
    private int height;
    private TETile[][] world;
    private TETile[][] bb;
    private Random rando;

    public Visualizer(int w, int h, TETile[][] wd, Random r, TETile[][] b) {
        width = w;
        height = h;
        world = wd;
        rando = r;
        bb = b;
    }

    private TETile randomwall() {
        int random = rando.nextInt(4);
        if (random == 0) {
            return Tileset.WALL;
        }
        if (random == 1) {
            return Tileset.WALL2;
        }
        if (random == 2) {
            return Tileset.WALL3;
        }
        if (random == 3) {
            return Tileset.WALL4;
        } else {
            return randomwall();
        }
    }

    //Hybridized.
    public void drawhalls(Room[] rooms) {
        for (Room room : rooms) {
            for (Room neighbor : room.getneighbors()) {
                if (neighbor != null && !room.contains(neighbor)) {
                    drawhall(room.getHallnode(), neighbor.getHallnode());
                    room.addAttachment(neighbor);
                    neighbor.addAttachment(room);
                } else {
                    continue;
                }
            }
        }
    }

    public void updateplayer(int[] coords) {
        int x = coords[0];
        int y = coords[1];
        world[x][y] = Tileset.PLAYER;
    }

    public void canvas() { //Creates the nothing background.
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                world[x][y] = randomwall();
                bb[x][y] = Tileset.NOTHING;
            }
        }
    }

    public void buildRooms(Room[] rooms) { //Builds the rooms visually on the map.
        for (Room room : rooms) {
            drawRoom(room.roomBP());
        }
    }

    private void drawRoom(int[][] room) {
        //First item is room dimensions, second is room origin, third is room node.
        int xcor = room[1][0];
        int ycor = room[1][1];
        int w = room[0][0];
        int h = room[0][1];
        for (int x = xcor; x < xcor + w; x++) {
            for (int y = ycor; y < ycor + h; y++) {
                if (x == xcor || y == ycor) {
                    world[x][y] = Tileset.WALL;
                } else if (x == xcor + w - 1 || y == ycor + h - 1) {
                    world[x][y] = Tileset.WALL;
                } else {
                    world[x][y] = Tileset.FLOOR;
                }
            }
        }
    }

    public void dotyourts(Room[] rooms) {
        //Testing purposes. Reveals HallwayNodes visually on the map.
        //In practice hallway nodes should be no different from regular
        //floor tiles visually.
        for (int i = 0; i < rooms.length; i++) {
            int[] coords = rooms[i].getHallnode();
            if (i == 0) {
                world[coords[0]][coords[1]] = Tileset.PLAYER;
            } else if (i < 5) {
                world[coords[0]][coords[1]] = Tileset.PORTAL;
            } else {
                world[coords[0]][coords[1]] = getfood();
            }

        }
    }

    private TETile getfood() {
        int random = rando.nextInt(3);
        if (random == 0) {
            return Tileset.FOOD1;
        }
        if (random == 1) {
            return Tileset.FOOD2;
        }
        if (random == 2) {
            return Tileset.FOOD3;
        } else {
            return getfood();
        }
    }

    //Visual. Monolithic. Must Edit.
    public void drawhall(int[] s, int[] e) {
        int startx = s[0];
        int starty = s[1];
        int endx = e[0];
        int endy = e[1];
        while (startx != endx) {
            if (startx >= endx) {
                world[startx - 1][starty] = Tileset.FLOOR;
                if (world[startx - 1][starty + 1] == Tileset.NOTHING) {
                    world[startx - 1][starty + 1] = Tileset.WALL;
                }
                if (world[startx - 1][starty - 1] == Tileset.NOTHING) {
                    world[startx - 1][starty - 1] = Tileset.WALL;
                }
                startx--;
            } else {
                world[startx + 1][starty] = Tileset.FLOOR;
                if (world[startx - 1][starty + 1] == Tileset.NOTHING) {
                    world[startx - 1][starty + 1] = Tileset.WALL;
                }
                if (world[startx - 1][starty - 1] == Tileset.NOTHING) {
                    world[startx - 1][starty - 1] = Tileset.WALL;
                }
                startx++;
            }
        }

        for (int i = starty - 1; i < starty + 1; i++) {
            if (world[startx][i] == Tileset.NOTHING) {
                world[startx][i] = Tileset.WALL;
            }
        }


        while (starty != endy) {
            if (starty > endy) {
                world[endx][starty - 1] = Tileset.FLOOR;
                if (world[endx + 1][starty - 1] == Tileset.NOTHING) {
                    world[endx + 1][starty - 1] = Tileset.WALL;
                }
                if (world[endx - 1][starty - 1] == Tileset.NOTHING) {
                    world[endx - 1][starty - 1] = Tileset.WALL;
                }
                starty--;
            } else {
                world[endx][starty + 1] = Tileset.FLOOR;
                if (world[endx + 1][starty - 1] == Tileset.NOTHING) {
                    world[endx + 1][starty - 1] = Tileset.WALL;
                }
                if (world[endx - 1][starty - 1] == Tileset.NOTHING) {
                    world[endx - 1][starty - 1] = Tileset.WALL;
                }
                starty++;
            }
        }

        for (int i = startx - 1; i < startx + 1; i++) {
            if (world[i][endy] == Tileset.NOTHING) {
                world[i][endy] = Tileset.WALL;
            }
        }
    }

}
