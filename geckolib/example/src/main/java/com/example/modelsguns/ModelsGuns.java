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

    public static final String[] GUNS = {"mk18", "glock17", "ak47", "deagle", "mp5a5", "m870", "awm"};

    @Override
    public void onInitialize() {
        for (String id : GUNS) {
            ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(MOD_ID, id));
            Registry.register(BuiltInRegistries.ITEM, key, new GunItem(id, new Item.Properties().setId(key).stacksTo(1)));
        }
    }
}
