package com.example.modelsguns;

import java.util.function.Consumer;

import com.geckolib.animatable.GeoItem;
import com.geckolib.animatable.client.GeoRenderProvider;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.animation.AnimationController;
import com.geckolib.animation.RawAnimation;
import com.geckolib.animation.object.PlayState;
import com.geckolib.model.DefaultedItemGeoModel;
import com.geckolib.renderer.GeoItemRenderer;
import com.geckolib.util.GeckoLibUtil;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import org.jspecify.annotations.Nullable;

/**
 * Gun item for Minecraft 26.2 + Fabric + GeckoLib 5 (Mojang names).
 *
 * GeckoLib loads:
 *   assets/<modid>/geckolib/models/item/<id>.geo.json
 *   assets/<modid>/geckolib/animations/item/<id>.animation.json
 *   assets/<modid>/textures/item/<id>.png
 * and the item is drawn through assets/<modid>/items/<id>.json
 * ("minecraft:special" -> "geckolib:geckolib"), whose base model
 * models/item/<id>.json holds the hand/GUI transforms.
 *
 * Two controllers:
 *   "state"  loops animation.<id>.idle (swap it for sprint / idle_empty from your own logic),
 *   "action" holds every one-shot animation of the gun as a triggerable animation
 *            (shoot, shoot_last, reload, reload_empty, inspect, draw, holster, ...).
 * Right click plays "shoot".
 */
public class GunItem extends Item implements GeoItem {
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
    private final String gunId;
    private final String[] actions;

    public GunItem(String gunId, String[] actions, Properties properties) {
        super(properties);
        this.gunId = gunId;
        this.actions = actions;
        GeoItem.registerSyncedAnimatable(this);
    }

    @Override
    public void createGeoRenderer(Consumer<GeoRenderProvider> consumer) {
        consumer.accept(new GeoRenderProvider() {
            private @Nullable GeoItemRenderer<GunItem> renderer;

            @Override
            public GeoItemRenderer<?> getGeoItemRenderer() {
                if (this.renderer == null) {
                    this.renderer = new GeoItemRenderer<>(new DefaultedItemGeoModel<>(
                            Identifier.fromNamespaceAndPath(ModelsGuns.MOD_ID, gunId)));
                }
                return this.renderer;
            }
        });
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        final RawAnimation idle = RawAnimation.begin().thenLoop("animation." + gunId + ".idle");
        controllers.add(new AnimationController<GunItem>("state", 4, test -> test.setAndContinue(idle)));

        final AnimationController<GunItem> action = new AnimationController<>("action", 0, test -> PlayState.STOP);
        for (String name : this.actions) {
            action.triggerableAnim(name, RawAnimation.begin().thenPlay("animation." + gunId + "." + name));
        }
        controllers.add(action);
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel serverLevel) {
            triggerAnim(player, GeoItem.getOrAssignId(stack, serverLevel), "action", "shoot");
        }
        return InteractionResult.SUCCESS;
    }
}
