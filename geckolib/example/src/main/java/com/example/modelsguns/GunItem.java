package com.example.modelsguns;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

import com.example.modelsguns.client.GunRenderer;
import com.example.modelsguns.client.GunState;
import com.geckolib.animatable.GeoItem;
import com.geckolib.animatable.client.GeoRenderProvider;
import com.geckolib.animatable.instance.AnimatableInstanceCache;
import com.geckolib.animatable.manager.AnimatableManager;
import com.geckolib.animation.AnimationController;
import com.geckolib.animation.RawAnimation;
import com.geckolib.animation.object.PlayState;
import com.geckolib.renderer.GeoItemRenderer;
import com.geckolib.util.GeckoLibUtil;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUseAnimation;
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
 *   "state"  loops idle / walk / sprint / aim (chosen on the client by GunState),
 *   "action" holds every one-shot animation of the gun as a triggerable animation
 *            (shoot, shoot_aim, dry_fire, dry_fire_aim, reload, reload_empty, inspect, ...).
 * Holding right click aims; releasing it fires an aimed shot.  A real mod would
 * fire from its own key and pick shoot / shoot_aim / dry_fire / dry_fire_aim
 * from the aim state and the ammo count.
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
            private @Nullable GunRenderer renderer;

            @Override
            public GeoItemRenderer<?> getGeoItemRenderer() {
                if (this.renderer == null) {
                    this.renderer = new GunRenderer(gunId);
                }
                return this.renderer;
            }
        });
    }

    private RawAnimation anim(String name, boolean loop) {
        String full = "animation." + this.gunId + "." + name;
        return loop ? RawAnimation.begin().thenLoop(full) : RawAnimation.begin().thenPlay(full);
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        Map<String, RawAnimation> loops = new HashMap<>();
        for (String name : new String[] {"idle", "walk", "sprint", "aim"}) {
            loops.put(name, anim(name, true));
        }
        // 5 ticks of blending between the loops gives smooth aim in / out and sprint tuck
        controllers.add(new AnimationController<GunItem>("state", 5,
                test -> test.setAndContinue(loops.get(GunState.loop(this)))));

        final AnimationController<GunItem> action = new AnimationController<>("action", 0, test -> PlayState.STOP);
        for (String name : this.actions) {
            action.triggerableAnim(name, anim(name, false));
        }
        controllers.add(action);
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return this.cache;
    }

    @Override
    public int getUseDuration(ItemStack stack, LivingEntity entity) {
        return 72000;
    }

    @Override
    public ItemUseAnimation getUseAnimation(ItemStack stack) {
        return ItemUseAnimation.NONE;
    }

    @Override
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        player.startUsingItem(hand);          // aim while right click is held
        return InteractionResult.CONSUME;
    }

    @Override
    public boolean releaseUsing(ItemStack stack, Level level, LivingEntity entity, int timeLeft) {
        if (level instanceof ServerLevel serverLevel && entity instanceof Player player) {
            triggerAnim(player, GeoItem.getOrAssignId(stack, serverLevel), "action", "shoot_aim");
        }
        return true;
    }
}
