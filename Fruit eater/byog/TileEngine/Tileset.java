package byog.TileEngine;

import java.awt.Color;

/**
 * Contains constant tile objects, to avoid having to remake the same tiles in different parts of
 * the code.
 *
 * You are free to (and encouraged to) create and add your own tiles to this file. This file will
 * be turned in with the rest of your code.
 *
 * Ex:
 *      world[x][y] = Tileset.FLOOR;
 *
 * The style checker may crash when you try to style check this file due to use of unicode
 * characters. This is OK.
 */

public class Tileset {
    public static final TETile PLAYER = new TETile('!', Color.YELLOW, Color.ORANGE, "player");
    public static final TETile WALL = new TETile('#', new Color(216, 128, 128),
            new Color(41, 8, 81),
            "wall");
    public static final TETile WALL2 = new TETile('#', new Color(136, 81, 216),
            new Color(41, 8, 81),
            "wall");
    public static final TETile WALL3 = new TETile('#', new Color(216, 19, 12),
            new Color(41, 8, 81),
            "wall");
    public static final TETile WALL4 = new TETile('#', new Color(117, 206, 216),
            new Color(41, 8, 81),
            "wall");
    public static final TETile FLOOR = new TETile('·', new Color(26, 124, 203),
            Color.black,
            "floor");
    public static final TETile PORTAL = new TETile('0', new Color(155, 12, 28),
            new Color(57, 6, 128),
            "portal (Teleports you!)");

    public static final TETile FOOD1 = new TETile('F', Color.GREEN,
            new Color(144, 255, 63),
            "Stone Melon (Eat through walls!)");

    public static final TETile FOOD2 = new TETile('B', Color.GREEN,
            new Color(240, 76, 182),
            "Honey Fruit (+30 movement!)");

    public static final TETile FOOD3 = new TETile('A', Color.white,
            new Color(16, 128, 81), "Light Berry (Increased Vision!)");


    public static final TETile NOTHING = new TETile(' ', Color.black, Color.black, "nothing");
    public static final TETile GRASS = new TETile('"', Color.green, Color.black, "grass");
    public static final TETile WATER = new TETile('≈', Color.blue, Color.black, "water");
    public static final TETile LAVA = new TETile('≈', Color.orange, Color.red, "water");
    public static final TETile FLOWER = new TETile('❀', Color.magenta, Color.pink, "flower");
    public static final TETile LOCKED_DOOR = new TETile('█', Color.orange, Color.black,
            "locked door");
    public static final TETile UNLOCKED_DOOR = new TETile('▢', Color.orange, Color.black,
            "unlocked door");
    public static final TETile SAND = new TETile('▒', Color.yellow, Color.black, "sand");
    public static final TETile MOUNTAIN = new TETile('▲', Color.gray, Color.black, "mountain");
    public static final TETile TREE = new TETile('♠', Color.green, Color.black, "tree");
}


