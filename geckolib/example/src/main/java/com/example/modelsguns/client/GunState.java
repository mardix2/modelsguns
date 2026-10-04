package com.example.modelsguns.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.world.item.ItemStack;

/**
 * Client-side choice of the looping animation for the gun in the local
 * player's hand: sprint > aim > walk > idle.  Kept in its own class so the
 * server never loads client classes.
 */
public final class GunState {
    private GunState() {}

    public static String loop(Object gun) {
        LocalPlayer player = Minecraft.getInstance().player;
        if (player == null) {
            return "idle";
        }
        ItemStack using = player.getUseItem();
        if (player.isSprinting()) {
            return "sprint";
        }
        if (player.isUsingItem() && using.getItem() == gun) {
            return "aim";
        }
        if (player.getDeltaMovement().horizontalDistanceSqr() > 0.0006 && player.onGround()) {
            return "walk";
        }
        return "idle";
    }
}
