package com.hearthsim.card.basic.minion;

import com.hearthsim.card.minion.AuraTargetType;
import com.hearthsim.card.minion.Minion;
import com.hearthsim.card.minion.MinionWithAura;
import com.hearthsim.model.BoardModel;
import com.hearthsim.model.PlayerSide;

import java.util.EnumSet;

public class GrimscaleOracle extends Minion implements MinionWithAura {

    public GrimscaleOracle() {
        super();
    }

    @Override
    public EnumSet<AuraTargetType> getAuraTargets() {
        return EnumSet.of(AuraTargetType.AURA_FRIENDLY_MINIONS, AuraTargetType.AURA_ENEMY_MINIONS);
    }

    @Override
    public void applyAura(PlayerSide targetSide, Minion targetMinion,
            BoardModel boardModel) {
        if (targetMinion.getTribe() == Minion.MinionTribe.MURLOC)
            targetMinion.setAuraAttack((byte)(targetMinion.getAuraAttack() + 1));
    }

    @Override
    public void removeAura(PlayerSide targetSide, Minion targetMinion,
            BoardModel boardModel) {
        if (targetMinion.getTribe() == Minion.MinionTribe.MURLOC)
            targetMinion.setAuraAttack((byte)(targetMinion.getAuraAttack() - 1));
    }

}
