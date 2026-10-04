package com.example.modelsguns;

import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;

public class ModelsGuns implements ModInitializer {
    public static final String MOD_ID = "modelsguns";

    /// one-shot animations (see the README for which gun has which; a name a
    /// gun does not have is simply never triggered for it)
    public static final String[] ACTIONS = {"shoot", "shoot_aim", "shoot_last", "dry_fire", "dry_fire_aim",
            "aim_in", "aim_out", "reload", "reload_empty", "reload_start", "reload_end", "pump", "bolt",
            "inspect", "firemode", "draw", "holster"};

    public static final String[] GUNS = {"mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm",
            "m1911", "m9a4", "p320", "mk23", "rhino"};

    @Override
    public void onInitialize() {
        for (String id : GUNS) {
            ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(MOD_ID, id));
            Registry.register(BuiltInRegistries.ITEM, key, new GunItem(id, ACTIONS, new Item.Properties().setId(key).stacksTo(1)));
        }
    }
}
