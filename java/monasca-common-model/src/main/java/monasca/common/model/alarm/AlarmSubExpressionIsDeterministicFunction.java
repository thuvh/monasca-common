/*
 * Copyright 2016 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

package monasca.common.model.alarm;

import java.util.List;

import javax.annotation.Nullable;

import com.google.common.base.Function;
import com.google.common.collect.Lists;
import org.antlr.v4.runtime.tree.ParseTree;

/**
 * Encapsulates {@link AlarmSubExpression#deterministic} detection logic.
 *
 * {@link Function} evaluates if deterministic from an expression
 * is just a keyword or an assignment operation.
 *
 * Logic is:
 * <ol>
 * <li>only <b>deterministic</b> keyword, return {@link Boolean#TRUE}</li>
 * <li>
 * assignment operator
 * <ol>
 * <li>verify if supplied value is valid, if not throw exception</li>
 * <li>check if value is one of {@link Boolean#TRUE} - like values, if so return
 * {@link Boolean#TRUE}</li>
 * <li>return {@link Boolean#FALSE} otherwise</li>
 * </ol>
 * </li>
 * </ol>
 */
enum AlarmSubExpressionIsDeterministicFunction
    implements Function<AlarmExpressionParser.DeterministicContext, Boolean> {

  INSTANCE {

    private final List<String> deterministicValues = Lists.newArrayList("1", "yes", "true");
    private final List<String> nonDeterministicValues = Lists.newArrayList("0", "no", "false");
    private final int deterministicValueIndex = 2;

    @Nullable
    @Override
    public Boolean apply(@Nullable final AlarmExpressionParser.DeterministicContext ctx) {

      if (ctx == null) {
        // should not actually happen, but @Nullable from Function interface
        // forces to check that, otherwise code here will produce compiler warning
        return AlarmSubExpression.DEFAULT_DETERMINISTIC;
      }

      final int childCount = ctx.getChildCount();

      if (childCount == 1) {
        // at this point, deterministic keyword was found in expression
        // and accepted by grammar rules, so just return true
        return true;
      }

      // 2nd possible option is assignment operator
      // everything else is forbidden by grammar for expression
      return this.handleAssignmentOperator(ctx);
    }

    private Boolean handleAssignmentOperator(final AlarmExpressionParser.DeterministicContext ctx) {
      final ParseTree child = ctx.getChild(this.deterministicValueIndex);
      final String text = child.getText().toLowerCase();

      if (this.isInvalidValue(text)) {
        throw new IllegalArgumentException(
            String.format(
                "%s is not valid deterministic value, one of %s or %s is expected",
                text,
                this.deterministicValues,
                this.nonDeterministicValues
            )
        );
      }

      return this.deterministicValues.contains(text);
    }

    private boolean isInvalidValue(final String text) {
      return !(this.deterministicValues.contains(text)
        || this.nonDeterministicValues.contains(text));
    }

  }

}
